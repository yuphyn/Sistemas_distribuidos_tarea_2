#!/usr/bin/env python
import pika
import time


def callback(ch, method, properties, body):
    mensaje = str(body)
    global usuarios
    mensaje=mensaje[2:-1].split(" ")
    if mensaje[0]=="registrar":
        usuarios[mensaje[1]]=[]
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        result = channel.queue_declare(queue=mensaje[1])
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs', queue=queue_name)
        connection.close()

    elif mensaje[0]=="usuarios":
        reenviar=mensaje[1]+" usuarios"
        for x in usuarios.keys():
            reenviar=reenviar+" "+x
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        channel.basic_publish(exchange='logs', routing_key='', body=reenviar)
        connection.close()

    elif mensaje[0]=="mensaje":
        reenviar=mensaje[1]+" mensaje"
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
        usuarios[mensaje[1]].append(("envio",mensaje[3]))
        usuarios[mensaje[2]].append(("recibo",mensaje[3]))
        log=open("log.txt","a")
        log.write("TIMESTAMP: "+mensaje[-1]+" ID_ORIGEN: "+mensaje[3]+" ID_DESTINO: "+mensaje[2]+" MENSAJE: ")
        
        mensaje__=""
        for x in mensaje[3:-1]:
            mensaje__=mensaje__+x+"_"
            log.write(x+" ")
        log.write("\n")
        log.close()
        reenviar=mensaje[2]+" mensajeee "+mensaje[1]+" "+mensaje__+" "+mensaje[-1]
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        channel.basic_publish(exchange='logs', routing_key='', body=reenviar)
        connection.close()


if __name__ == "__main__":
    log=open("log.txt","w")
    log.close()
    usuarios={}
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)
    print('Server running')
    channel.start_consuming()
