"""The Python implememntation of seans grpc client"""
import os
import time
import grpc
import tarea_pb2
import tarea_pb2_grpc
import time
import threading


if os.environ.get('https_proxy'):
    del os.environ['https_proxy']
if os.environ.get('http_proxy'):
    del os.environ['http_proxy']

class run():
    "The run method, that sends gRPC conformant messsages to the server"
    def __init__(self):
        print("init")
        self.channel = grpc.insecure_channel("localhost:9999")
        self.stub = tarea_pb2_grpc.TareaStub(self.channel)
        self.user_id = 0
        self.current_users = []
        self.Ingresar()

    def __str__(self):
        return self.__class__.__name__

    def EnviarMensaje(self):
        while True:
            ingreso = input()
            data = ingreso.split(" ")
            if data[0]=="usuarios":
                self.ObtenerUsuarios()
            elif data[0]=="mensajes":
                self.ObtenerMensajes()
            else:
                mensaje = tarea_pb2.Mensaje(
					id_ori = self.user_id,
					id_des = int(data[0]),
					mensaje = ' '.join(data[1:]),
                    time = time.time()
				)
                self.ObtenerUsuarios()
                if int(data[0]) in self.current_users:
                    self.stub.EnviarMensaje(mensaje)
                else:
                    print("Usuario no existente")
    
    def RecibirMensaje(self):
        while True:
            time.sleep(1)
            request = tarea_pb2.ID(
				id = self.user_id
			)
            response = self.stub.RecibirMensaje(request)
            if response.mensaje != "FUERA PINERA":
                print('ID_origen ' + str(response.id_ori) + ' MENSAJE: ' + response.mensaje)
    
    def ObtenerUsuarios(self):
        request = tarea_pb2.Vacio()
        response = self.stub.ObtenerUsuarios(request)
        usuario = response.data
        usuarios =usuario.split(" ")
        print('Usuarios:')
        for x in usuarios:
            if x != " ":
                if x != "":
                    self.current_users.append(int(x))
                    print(x+"\n")
        print(self.current_users)


    def ObtenerMensajes(self):
        request = tarea_pb2.ID(
            id = self.user_id
        )
        response = self.stub.ObtenerMensajes(request)
        mensaje = response.data
        mensajes = mensaje.split("-------")
        for x in mensajes:
            print(x+"\n")

    def AgregarUsuario(self):
        request = tarea_pb2.Vacio()
        response = self.stub.AgregarUsuario(request)
        self.user_id=response.id
        print('Bienvenido, eres el usurio con ID: '+str(self.user_id)+"\n")
        print('Para ver los usuarios conectador ingresar: "usuarios"\n')
        print('para ver los mensajes enviados ingresar: "mensajes"\n')
        print('para enviar un mensaje ingresar: "(ID_destino) (MENSAJE)"')
        
    def Ingresar(self):
        self.AgregarUsuario()
        t1 = threading.Thread(target=self.EnviarMensaje)
        t2 = threading.Thread(target=self.RecibirMensaje)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    


                



def close(channel):
    "Close the channel"
    channel.close()


if __name__ == "__main__":
    run()
