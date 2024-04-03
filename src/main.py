import asyncio

import grpc
from psycopg2.pool import ThreadedConnectionPool

from src.application.configuration import ApplicationConfiguration
from src.application.proto.transaction_pb2_grpc import add_TransactionServicer_to_server
from src.application.service import TransactionService
from src.database.configuration import DatabaseConfiguration
from src.grpc_.server import GRPCServer


def on_startup(context: dict):
    ...


def on_shutdown(context: dict):
    ...


def create_server() -> grpc.aio.Server:
    database_configuration = DatabaseConfiguration.from_env()
    db_connection_pool = ThreadedConnectionPool(
        minconn=3,
        maxconn=10,
        user=database_configuration.user,
        database=database_configuration.database,
        password=database_configuration.password,
        host=database_configuration.host,
        port=int(database_configuration.port),
    )
    service = TransactionService(
        db_connection_pool=db_connection_pool,
    )

    application_configuration = ApplicationConfiguration.from_env()
    server = GRPCServer(
        host=application_configuration.host,
        port=application_configuration.port,
    )
    server.on_startup = on_startup
    server.on_shutdown = on_shutdown

    add_TransactionServicer_to_server(service, server)

    return server


async def main():
    server = create_server()
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())
