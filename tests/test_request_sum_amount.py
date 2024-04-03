import grpc
import pytest
from psycopg2._psycopg import connection

from src.application.proto import transaction_pb2
from src.application.proto import transaction_pb2_grpc


async def test_sum_amount_one_and_one(
        db_connection: connection,
        grpc_channel: grpc.Channel,
        create_transaction_table,
):
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2), (1, 1, 2)')
    db_connection.commit()
    async with grpc_channel:
        stub = transaction_pb2_grpc.TransactionStub(grpc_channel)
        response = await stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
            user_id=1,
            start_from=1,
            end_from=3,
        ))
    assert response.value == 2


async def test_out_of_range_timestamp(
        db_connection: connection,
        grpc_channel: grpc.Channel,
        create_transaction_table,
):
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2), (1, 1, 2)')
    db_connection.commit()
    async with grpc_channel:
        stub = transaction_pb2_grpc.TransactionStub(grpc_channel)
        with pytest.raises(grpc.aio.AioRpcError) as exc:
            await stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
                user_id=1,
                start_from=4,
                end_from=3,
            ))
        assert exc.value.code() == grpc.StatusCode.INVALID_ARGUMENT


async def test_not_existing_user(
        db_connection: connection,
        grpc_channel: grpc.Channel,
        create_transaction_table,
):
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2)')
    db_connection.commit()
    async with grpc_channel:
        stub = transaction_pb2_grpc.TransactionStub(grpc_channel)
        with pytest.raises(grpc.aio.AioRpcError) as exc:
            await stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
                user_id=2,
                start_from=1,
                end_from=2,
            ))
        assert exc.value.code() == grpc.StatusCode.INVALID_ARGUMENT
