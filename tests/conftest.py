from concurrent import futures

import grpc
import psycopg2
import psycopg2.pool
import pytest
import testing.postgresql

from src.application.proto.transaction_pb2_grpc import add_TransactionServicer_to_server
from src.application.service import TransactionService


@pytest.fixture(scope='package')
def postgresql():
    postgresql = testing.postgresql.Postgresql()
    yield postgresql
    postgresql.stop()


@pytest.fixture(scope='package')
def db_connection_pool(postgresql: testing.postgresql.Postgresql):
    db_connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=3, maxconn=10, dsn=postgresql.url())
    yield db_connection_pool
    db_connection_pool.closeall()


@pytest.fixture(scope='function')
def db_connection(db_connection_pool):
    db_connection = db_connection_pool.getconn()
    yield db_connection
    db_connection_pool.putconn(db_connection)


@pytest.fixture(scope='function')
def create_transaction_table(db_connection_pool):
    with open('migrations/1_create_transaction_table.sql') as file:
        migration = file.read()
    db_connection = db_connection_pool.getconn()
    with db_connection.cursor() as cursor:
        cursor.execute(migration)
    db_connection.commit()
    db_connection_pool.putconn(db_connection)
    yield
    with open('migrations/1_drop_transaction_table.sql') as file:
        migration = file.read()
    db_connection = db_connection_pool.getconn()
    with db_connection.cursor() as cursor:
        cursor.execute(query=migration)
    db_connection.commit()
    db_connection_pool.putconn(db_connection)


@pytest.fixture(scope='function')
def grpc_channel(db_connection):
    service = TransactionService(
        db_connection_factory=lambda: db_connection,
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TransactionServicer_to_server(service, server)
    server.add_insecure_port('localhost:50501')
    server.start()
    yield grpc.insecure_channel('localhost:50501')
    server.stop(None)
