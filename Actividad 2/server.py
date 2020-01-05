#!/usr/bin/env python
import pika
import time


def callback(ch, method, properties, body):
    mensaje = str(body)
    global usuarios
    mensaje=mensaje[2:-1].split(" ")
    if mensaje[0]=="registrar":
        time.sleep(10)
        usuarios[mensaje[1]]=[]
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        result = channel.queue_declare(queue=mensaje[1], exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs', queue=queue_name)
        connection.close()

    if mensaje[0]=="usuarios":
        reenviar=mensaje[1]
        for x in usuarios.keys():
            reenviar=reenviar+" "+x
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        channel.basic_publish(exchange='logs', routing_key='', body=reenviar)
        connection.close()

    elif mensaje[0]=="mensaje":
        reenviar=mensaje[1]
        for x,y in usuarios.items():
            if x==mensaje[1]:
                for a,b in y:
                    if a=="envio":
                        reenviar=reenviar+" "+b
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        channel.basic_publish(exchange='logs', routing_key='', body=reenviar)
        connection.close()

    else:
        usuarios[mensaje[1]].append("envio",mensaje[4])
        usuarios[mensaje[2]].append("recibo",mensaje[4])

        log=open("log.txt","a")
        log.write("TIMESTAMP: "+mensaje[5]+" ID_ORIGEN: "+mensaje[2]+" ID_DESTINO: "+mensaje[3]+" MENSAJE: "+mensaje[4])
        log.close()
        reenviar=mensaje[2]+" mensaje "+mensaje[1]+" "+mensaje[3]+" "+mensaje[4]
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        channel.basic_publish(exchange='logs', routing_key='', body=mensaje)
        connection.close()


if __name__ == "__main__":
    usuarios={}
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)
    print('Server running')
    channel.start_consuming()
