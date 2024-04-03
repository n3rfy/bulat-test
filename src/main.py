from concurrent import futures

import grpc
from psycopg2.pool import ThreadedConnectionPool

from src.application.configuration import ApplicationConfiguration
from src.application.proto.transaction_pb2_grpc import add_TransactionServicer_to_server
from src.application.service import TransactionService
from src.database.configuration import DatabaseConfiguration


def create_server(configuration: ApplicationConfiguration) -> grpc.Server:
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

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TransactionServicer_to_server(service, server)
    server.add_insecure_port(f'{configuration.host}:{configuration.port}')
    return server


if __name__ == '__main__':
    application_configuration = ApplicationConfiguration.from_env()
    server = create_server(configuration=application_configuration)
    server.start()
    server.wait_for_termination()
