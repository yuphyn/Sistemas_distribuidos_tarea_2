"""The Python implementation of the GRPC Seans-gRPC server."""
from concurrent import futures
import threading
import time
import grpc
import tarea_pb2
import tarea_pb2_grpc

class Listener(tarea_pb2_grpc.TareaServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.id = 0

    def __str__(self):
        return self.__class__.__name__

    def ping(self, request, context):
        return tarea_pb2.Pong(id=request.id+1)


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    tarea_pb2_grpc.add_TareaServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:9999")
    server.start()
    try:
        while True:
            print("Server Running : threadcount %i" % (threading.active_count()))
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)


if __name__ == "__main__":
    serve()
