"""The Python implememntation of seans grpc client"""
import os
import time
import grpc
import tarea_pb2
import tarea_pb2_grpc
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
        self.FLAG=0
        self.Ingresar()

    def __str__(self):
        return self.__class__.__name__

    def EnviarMensaje(self):
        while True:
            ingreso = input()
            if ingreso=="1":
                self.ObtenerUsuarios()
            elif ingreso=="2":
                self.ObtenerMensajes()
            elif ingreso=="3":
                ingreso2 = input("Ingrese mensaje de la siguiente forma: (ID_destino) (MENSAJE):\n")
                data = ingreso2.split(" ")
                t = time.time()
                timestamp_final = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(t))
                mensaje = tarea_pb2.Mensaje(
					id_ori = self.user_id,
					id_des = int(data[0]),
					mensaje = ' '.join(data[1:]),
                    time = timestamp_final
				)
                self.FLAG=1
                self.ObtenerUsuarios()
                self.FLAG=0
                if int(data[0]) == self.user_id:
                    print("No te puedes mandar un mensaje a ti mismo")
                elif int(data[0]) in self.current_users:
                    self.stub.EnviarMensaje(mensaje)
                else:
                    print("Usuario no existente")
            else:
                print("Comando no valido")
    
    def RecibirMensaje(self):
        while True:
            time.sleep(1)
            request = tarea_pb2.ID(
				id = self.user_id
			)
            response = self.stub.RecibirMensaje(request)
            if response.id_ori != -1:
                print('FECHA: '+ str(response.time)+' ID_origen: ' + str(response.id_ori) + ' MENSAJE: ' + response.mensaje)
    
    def ObtenerUsuarios(self):
        request = tarea_pb2.Vacio()
        response = self.stub.ObtenerUsuarios(request)
        usuario = response.data
        usuarios =usuario.split(" ")
        if self.FLAG==0:
            print('Usuarios:')
        for x in usuarios:
            if x != " ":
                if x != "":
                    self.current_users.append(int(x))
                    if self.FLAG==0:
                        print(x)


    def ObtenerMensajes(self):
        request = tarea_pb2.ID(
            id = self.user_id
        )
        response = self.stub.ObtenerMensajes(request)
        mensaje = response.data
        mensajes = mensaje.split("-------")
        print('Mensajes:')
        for x in mensajes:
            print(x)

    def AgregarUsuario(self):
        request = tarea_pb2.Vacio()
        response = self.stub.AgregarUsuario(request)
        self.user_id=response.id
        print('Bienvenido, eres el usurio con ID: '+str(self.user_id))
        print('Para ver los usuarios conectador ingresar: 1')
        print('para ver los mensajes enviados ingresar: 2')
        print('para enviar un mensaje ingresar: 3')
        
    def Ingresar(self):
        self.AgregarUsuario()
        t1 = threading.Thread(target=self.EnviarMensaje)
        t2 = threading.Thread(target=self.RecibirMensaje)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    run()
