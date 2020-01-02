# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import tarea_pb2 as tarea__pb2


class TareaStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ping = channel.unary_unary(
        '/Tarea/ping',
        request_serializer=tarea__pb2.Ping.SerializeToString,
        response_deserializer=tarea__pb2.Pong.FromString,
        )


class TareaServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ping(self, request, context):
    """Sends a greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TareaServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ping': grpc.unary_unary_rpc_method_handler(
          servicer.ping,
          request_deserializer=tarea__pb2.Ping.FromString,
          response_serializer=tarea__pb2.Pong.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Tarea', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
