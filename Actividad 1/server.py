"""The Python implementation of the GRPC Seans-gRPC server."""
from concurrent import futures
import os
import threading
import time
import grpc
import tarea_pb2
import tarea_pb2_grpc

if os.environ.get('https_proxy'):
    del os.environ['https_proxy']
if os.environ.get('http_proxy'):
    del os.environ['http_proxy']

class Listener(tarea_pb2_grpc.TareaServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.users = {}
        self.contador=0
        self.last = []

    def __str__(self):
        return self.__class__.__name__

    def AgregarUsuario(self, request, context):
        id_user=self.contador
        self.users[id_user] = []
        self.contador+=1
        id = tarea_pb2.ID(
            id = id_user
        )

        return id

    def EnviarMensaje(self, request, context):
        id_origen = request.id_ori
        id_destino = request.id_des
        mensaje = request.mensaje
        timestamp = request.time

        
        lod = open('log.txt', 'a')
        lod.write('TIMESTAMP: '+ str(time) +' ID_origen: ' + str(id_origen) + ' ID_destino: ' + str(id_destino) + ' MENSAJE: ' + mensaje +'\n')
        lod.close()
        self.users[id_origen].append(('envio',mensaje))
        self.users[id_destino].append(('recibo',mensaje))

        self.last.append((id_destino,id_origen,timestamp,mensaje))

        vacio = tarea_pb2.Vacio()

        return vacio


    def RecibirMensaje(self, request, context):
        id_destino = request.id
        i=0
        for x,y,z,w in self.last:
            if x==id_destino:
                id_origen=y
                mensaje=w
                timestamp=z
                self.last.remove((x,y,z,w))
                i=1
        
        if i==1:
            mensaje = tarea_pb2.Mensaje(
                id_ori = id_origen,
                id_des = id_destino,
                mensaje = mensaje,
                time = timestamp
            )
        else:
            mensaje = tarea_pb2.Mensaje(
                id_ori = 0,
                id_des = id_destino,
                mensaje = "FUERA PINERA",
                time = 0.0
            )
        
        return mensaje

    def ObtenerUsuarios(self, request, context):
        total = ''
        for x in self.users.keys():
            total=total+str(x)+' '

        data = tarea_pb2.Data(
            data = total
        )
        return data

    def ObtenerMensajes(self, request, context):
        total = ''
        for x in self.users.items():
            if x[0]==request.id:
                for y,z in x[1]:
                    if y=="envio":
                        total=total+z+'-------'

        data = tarea_pb2.Data(
            data = total
        )
        return data


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""
    log = open('log.txt', 'w')
    log.close()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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
