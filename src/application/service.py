import time
from dataclasses import dataclass
from typing import Callable
from typing import Mapping
from typing import cast

import grpc
import psycopg2
from psycopg2._psycopg import connection

from src.application.proto import transaction_pb2
from src.application.proto.transaction_pb2_grpc import TransactionServicer


CALCULATE_USER_TOTAL_SUM = '''
select sum(transaction.amount) as sum_amount
from transaction
where transaction.user_id = %s
    and transaction.timestamp between %s and %s
'''


@dataclass
class CalculateUserTotalSumRequest:
    user_id: str
    start_from: str
    end_from: str


class TransactionService(TransactionServicer):
    def __init__(self, db_connection_factory: Callable[[], connection]) -> None:
        self._create_db_connection = db_connection_factory

    def sum_amount(self, request: CalculateUserTotalSumRequest, context):
        start_time = time.monotonic()
        if request.start_from > request.end_from:
            context.set_details('INVALID_TIME_RANGE')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return

        try:
            db_connection = self._create_db_connection()
            with db_connection.cursor() as cursor:
                cursor.execute(
                    query=CALCULATE_USER_TOTAL_SUM,
                    vars=(request.user_id, request.start_from, request.end_from))
                amount = cast(Mapping, cursor.fetchone())[0]
            db_connection.close()
        except psycopg2.Error:
            context.set_details('DATABASE_ERROR')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        if amount is None:
            context.set_details('INVALID_USER_ID')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return

        execution_time_in_seconds = time.monotonic() - start_time
        execution_time_in_milliseconds = int(execution_time_in_seconds * 1000)

        return transaction_pb2.CalculateUserTotalSumResponse(
            value=amount,
            execution_time=execution_time_in_milliseconds,
        )
