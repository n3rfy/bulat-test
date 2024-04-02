import psycopg2

from src.database.configuration import DatabaseConfiguration


def create_db_connection_factory(database_config: DatabaseConfiguration):
    def create_db_connection():
        return psycopg2.connect(
            user=database_config.user,
            database=database_config.database,
            password=database_config.password,
            host=database_config.host,
            port=int(database_config.port),
        )

    return create_db_connection
