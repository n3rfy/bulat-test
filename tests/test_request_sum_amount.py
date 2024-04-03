import grpc
import pytest

from src.application.proto import transaction_pb2
from src.application.proto import transaction_pb2_grpc


def test_sum_amount_one_and_one(
        create_transaction_table,
        create_grpc_server,
        db_connection_pool,
):
    db_connection = db_connection_pool.getconn()
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2), (1, 1, 2)')
    db_connection.commit()
    db_connection_pool.putconn(db_connection)
    with grpc.insecure_channel(f'localhost:50501') as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        response = stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
            user_id=1,
            start_from=1,
            end_from=3
        ))
    assert response.value == 2


def test_out_of_range_timestamp(
        create_transaction_table,
        create_grpc_server,
        db_connection_pool,
):
    db_connection = db_connection_pool.getconn()
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2), (1, 1, 2)')
    db_connection.commit()
    db_connection_pool.putconn(db_connection)
    with grpc.insecure_channel(f'localhost:50501') as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        with pytest.raises(grpc.RpcError) as exc:
            stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
                user_id=1,
                start_from=4,
                end_from=3
            ))
        assert exc.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_not_existing_user(
        create_transaction_table,
        create_grpc_server,
        db_connection_pool,
):
    db_connection = db_connection_pool.getconn()
    with db_connection.cursor() as cursor:
        cursor.execute(query='insert into transaction (user_id, amount, timestamp) values (1, 1, 2)')
    db_connection.commit()
    db_connection_pool.putconn(db_connection)
    with grpc.insecure_channel(f'localhost:50501') as channel:
        stub = transaction_pb2_grpc.TransactionStub(channel)
        with pytest.raises(grpc.RpcError) as exc:
            stub.sum_amount(transaction_pb2.CalculateUserTotalSumRequest(
                user_id=2,
                start_from=1,
                end_from=2
            ))
        assert exc.value.code() == grpc.StatusCode.INVALID_ARGUMENT
