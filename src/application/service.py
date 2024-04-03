import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

import grpc
import psycopg2
from psycopg2.pool import ThreadedConnectionPool

from src.application.proto import transaction_pb2
from src.application.proto.transaction_pb2_grpc import TransactionServicer


@dataclass
class CalculateUserTotalSumRequest:
    user_id: str
    start_from: str
    end_from: str


class TransactionService(TransactionServicer):
    def __init__(self, db_connection_pool: ThreadedConnectionPool) -> None:
        self._db_connection_pool = db_connection_pool

    def sum_amount(self, request: CalculateUserTotalSumRequest, context):
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
