"""The Python implememntation of seans grpc client"""
import os
import time
import grpc
import tarea_pb2
import tarea_pb2_grpc

def run():
    "The run method, that sends gRPC conformant messsages to the server"
    id = 2000
    pid = os.getpid()
    with grpc.insecure_channel("localhost:9999") as channel:
        stub = tarea_pb2_grpc.TareaStub(channel)
        while True:
            try:
                start = time.time()
                response = stub.ping(tarea_pb2.Ping(id=id))
                id = response.id
                if id % 1000 == 0:
                    print(
                        "%.4f : resp=%s : procid=%i"
                        % (time.time() - start, response.id, pid)
                    )
                    # counter = 0
                time.sleep(0.001)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                channel.unsubscribe(close)
                exit()


def close(channel):
    "Close the channel"
    channel.close()


if __name__ == "__main__":
    run()
