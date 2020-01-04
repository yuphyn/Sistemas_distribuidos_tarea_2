import pika
import threading
import time
import random


def crear_canal():
    params = pika.ConnectionParameters('localhost')
    conexion = pika.BlockingConnection(params)
    canal = conexion.channel()
    canal.basic_qos(prefetch_count=1)
    return canal

canal = crear_canal()

def recibir(ch, method, properties, body):
    mensaje = body.decode('UTF-8')
    print(mensaje)

def Enviar(mensaje, destino, user, canal):
    texto = user + ": " + mensaje + "#" + destino
    canal.basic_publish(exchange='', routing_key='envios', body=texto)

def Lista(user):
    canal.basic_publish(exchange='', routing_key='listas', body=user)

def Chat(user):
    user = str(user)
    canal.basic_publish(exchange='', routing_key='chats', body=user)


while True:
    user = input("Ingrese nombre de usuario: ")
    if user == "" or user == "?all":
        print("Ingresa un nombre de usuario valido")
    else:
        ver = str(random.randrange(100))
        ver = ver + " " + user
        canal.queue_declare(queue=str(ver))
        canal.basic_publish(exchange='', routing_key='confirmacion', body=ver)
        time.sleep(1)
        met, prop, body = canal.basic_get(queue=ver, auto_ack=True)
        body = body.decode('UTF-8')
        if body == "1":
            canal.queue_declare(queue=user)
            canal.queue_delete(queue=ver)
            print("Usuario registrado")
            break
        else:
            canal.queue_delete(queue=ver)
            print("Nombre ya utilizado")

envios = crear_canal()
envios.basic_consume(queue=user,on_message_callback=recibir,auto_ack=True)
threading.Thread(target=envios.start_consuming).start()

print("Ingrese su comando")
mens = str(input())
while mens != "?close":
    if len(mens.split(" ")) > 1:
        destino, mensaje = mens.split(" ",1)
        Enviar(mensaje, destino, user, canal)
    elif mens == "?list":
        Lista(user)
    elif mens == "?chat":
        Chat(user)
    else:
        print("Formato incorrecto")
    mens = str(input())

canal.basic_publish(exchange='', routing_key='desconexiones', body=user)
canal.queue_delete(queue=user)
# envios.close()
# canal.close()