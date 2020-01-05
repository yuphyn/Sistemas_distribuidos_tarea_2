import pika
import threading
import time

def EnviarMensaje():
    while True:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        global user_id
        channel.queue_declare(queue='hello')
        opcion = input()
        if opcion=="1":
            mensaje="usuarios "+str(user_id)
            channel.basic_publish(exchange='', routing_key='hello', body=mensaje)
        elif opcion=="2":
            mensaje="mensajes"+str(user_id)
            channel.basic_publish(exchange='', routing_key='hello', body=mensaje)
        elif opcion=="3":
            ingreso2 = input("Ingrese mensaje de la siguiente forma: (ID_destino) (MENSAJE):\n")
            t = time.time()
            timestamp_final = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(t))
            mensaje="enviar "+str(user_id)+" "+ingreso2+timestamp_final
            channel.basic_publish(exchange='', routing_key='hello', body=mensaje)
        else:
            print("opcion no valida")
        connection.close()

def RecibirMensaje():
    global user_id
    def callback(ch, method, properties, body):
        mensaje=body.split(" ")
        if mensaje[0]==user_id:
            if mensaje[1]=="mensaje":
                print(mensaje[4]+" ID_ORIGEN: "+mensaje[2]+ "MENSAJE: "+mensaje[3])
            else:
                contenido=mensaje[1:]
                for x in contenido:
                    print(x)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue=user_id, exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    user_id = input("Nuestro sistema necesita su rut para registrar un ID. Por favor ingrese su rut sin dv:\n")
    mensaje="registrar "+user_id
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=mensaje)
    connection.close()

    tRecibir = threading.Thread(target=RecibirMensaje)
    tEnviar = threading.Thread(target=EnviarMensaje)
    tRecibir.start()
    tEnviar.start()