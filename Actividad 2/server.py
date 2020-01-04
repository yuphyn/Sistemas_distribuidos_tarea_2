import pika
from datetime import datetime
import threading
import uuid
import time

params = pika.ConnectionParameters('localhost')
conexion = pika.BlockingConnection(params)
canal = conexion.channel()
canal.basic_qos(prefetch_count=1)

USERS = list()
CHATS = list()
lock_usuarios = threading.Lock()
lock_chat = threading.Lock()

def get_ts():
    tiempo = datetime.now()
    tiempo = tiempo.time().strftime("%H:%M:%S")
    return tiempo

canal.queue_declare(queue='registrar', durable=True)
canal.queue_declare(queue='envios')
canal.queue_declare(queue='confirmacion')
canal.queue_declare(queue='listas')
canal.queue_declare(queue='chats')
canal.queue_declare(queue='desconexiones')

def registro(ch, method, properties, body):
    user = body.decode('UTF-8')
    lock_usuarios.acquire()
    if user not in USERS:
        print("# Registrado", user)
        USERS.append(user)
        canal.queue_declare(queue=user, durable=True)
    lock_usuarios.release()

def enviar(ch, method, properties, body):
    lock_chat.acquire()
    log = open("log.txt","a+")
    body = body.decode('UTF-8')
    payload = body.split("#")
    mensaje = payload[0]
    mensaje = "(" + str(uuid.uuid1()) + ") " + mensaje
    mensaje = "[" + get_ts() + "] " + mensaje
    destino = payload[1]
    canal.basic_publish(exchange='', routing_key=destino, body=mensaje)
    print(mensaje)
    CHATS.append((mensaje,payload[0].split(":")[0]))
    log.write(mensaje + " -> " + destino + "\n")
    lock_chat.release()

def confirmar(ch, method, properties, body):
    lock_usuarios.acquire()
    body = body.decode('UTF-8')
    name = body.split(" ")[1]
    print("USERS: ", USERS)
    print("POR CONFIRMAR: ",body)
    if name not in USERS:
        canal.basic_publish(exchange='', routing_key=body, body="1")
        USERS.append(name)
    else:
        canal.basic_publish(exchange='', routing_key=body, body="0")
    lock_usuarios.release()


def lista(ch, method, properties, body):
    lock_usuarios.acquire()
    mensaje = str(USERS)
    canal.basic_publish(exchange='', routing_key=body, body=mensaje)
    lock_usuarios.release()

def chat(ch, method, properties, body):
    lock_chat.acquire()
    user = body.decode('UTF-8')
    historial = list()
    for mensaje in CHATS:
        if mensaje[1] == user:
            historial.append(mensaje[0])
    canal.basic_publish(exchange='', routing_key=user, body=str(historial))
    lock_chat.release()

def desconectar(ch, method, properties, body):
    lock_usuarios.acquire()
    user = body.decode('UTF-8')
    USERS.remove(user)
    print("Usuario {} desconectado".format(user))
    lock_usuarios.release()

print("CTRL+C para salir")
print("# Esperando por usuarios a conectarse...")

try:
    canal.basic_consume(queue='registrar', on_message_callback=registro, auto_ack=True)
    canal.basic_consume(queue='envios', on_message_callback=enviar, auto_ack=True)
    canal.basic_consume(queue='confirmacion', on_message_callback=confirmar, auto_ack=True)
    canal.basic_consume(queue='listas', on_message_callback=lista, auto_ack=True)
    canal.basic_consume(queue='chats', on_message_callback=chat, auto_ack=True)
    canal.basic_consume(queue='desconexiones', on_message_callback=desconectar, auto_ack=True)
    canal.start_consuming()
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    canal.close()
    conexion.close()