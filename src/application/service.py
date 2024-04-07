import time
from collections.abc import Mapping
from typing import cast

import grpc
import psycopg2
import structlog
from psycopg2.pool import ThreadedConnectionPool

from src.application.proto import transaction_pb2
from src.application.proto.transaction_pb2_grpc import TransactionServicer


logger: structlog.stdlib.BoundLogger = structlog.get_logger()


class TransactionService(TransactionServicer):
    def __init__(self, db_connection_pool: ThreadedConnectionPool) -> None:
        self._db_connection_pool = db_connection_pool

    def sum_amount(
            self,
            request: transaction_pb2.CalculateUserTotalSumRequest,
            context: grpc.ServicerContext,
    ) -> transaction_pb2.CalculateUserTotalSumResponse:
        start_time = time.perf_counter()
        if request.start_from > request.end_from:
            context.set_details('INVALID_TIME_RANGE')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None

        try:
            db_connection = self._db_connection_pool.getconn()
            with db_connection.cursor() as cursor:
                cursor.execute(
                    query='''
                        select sum(transaction.amount) as sum_amount
                        from transaction
                        where transaction.user_id = %s
                            and transaction.timestamp between %s and %s
                    ''',
                    vars=(request.user_id, request.start_from, request.end_from))
                amount = cast(Mapping, cursor.fetchone())[0]
            self._db_connection_pool.putconn(db_connection)
        except psycopg2.Error:
            context.set_details('DATABASE_ERROR')
            context.set_code(grpc.StatusCode.INTERNAL)
            logger.exception('DATABASE_ERROR')
            return None

        if amount is None:
            context.set_details('INVALID_USER_ID')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return None

        execution_time_in_seconds = time.perf_counter() - start_time
        execution_time_in_milliseconds = int(execution_time_in_seconds * 1000)

        return transaction_pb2.CalculateUserTotalSumResponse(
            value=amount,
            execution_time=execution_time_in_milliseconds,
        )
