# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.application.proto.transaction_pb2 as transaction__pb2


class TransactionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sum_amount = channel.unary_unary(
                '/transaction.Transaction/sum_amount',
                request_serializer=transaction__pb2.CalculateUserTotalSumRequest.SerializeToString,
                response_deserializer=transaction__pb2.CalculateUserTotalSumResponse.FromString,
                )


class TransactionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sum_amount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sum_amount': grpc.unary_unary_rpc_method_handler(
                    servicer.sum_amount,
                    request_deserializer=transaction__pb2.CalculateUserTotalSumRequest.FromString,
                    response_serializer=transaction__pb2.CalculateUserTotalSumResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'transaction.Transaction', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Transaction(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def sum_amount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transaction.Transaction/sum_amount',
            transaction__pb2.CalculateUserTotalSumRequest.SerializeToString,
            transaction__pb2.CalculateUserTotalSumResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
