from concurrent import futures

import grpc

from src.application.configuration import ApplicationConfiguration
from src.application.proto.transaction_pb2_grpc import add_TransactionServicer_to_server
from src.application.service import TransactionService
from src.database.configuration import DatabaseConfiguration
from src.database.connection_factory import create_db_connection_factory


if __name__ == '__main__':
    database_configuration = DatabaseConfiguration.from_env()
    db_connection_factory = create_db_connection_factory(database_config=database_configuration)
    service = TransactionService(
        db_connection_factory=db_connection_factory
    )

    application_configuration = ApplicationConfiguration.from_env()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TransactionServicer_to_server(service, server)
    server.add_insecure_port(f'{application_configuration.host}:{application_configuration.port}')
    server.start()
    server.wait_for_termination()
