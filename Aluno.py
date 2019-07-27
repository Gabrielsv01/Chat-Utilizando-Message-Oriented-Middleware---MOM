#!/usr/bin/env python
import pika
from threading import Thread
import time


class TH_server(Thread):

    def __init__ (self, num):
        Thread.__init__(self)
        self.num = num
    
    def run(self):

        def callback(ch, method, properties, body):

            print("                         %s" % body.decode())
            print("\n")

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='servidor')
        channel.basic_consume(queue='servidor', on_message_callback=callback, auto_ack=True)

        print('\n ###### Online ###### \n')
        print('Chat Ativo: \n')
        channel.start_consuming()



class TH_send(Thread):

    def __init__ (self, num):
        Thread.__init__(self)
        self.num = num
    
    def run(self):
        # estabelecendo conexao
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # conectando o canal
        channel = connection.channel()

        # declarando a chave do canal
        channel.queue_declare(queue='hello')

        # envio de mensagem
        def Enviar(canal,mensagem):

            canal.basic_publish(exchange='', routing_key='hello', body= mensagem)

        # finalizando conexao
        def Sair(conexao):
            conexao.close()

        while True:

            time.sleep(1)
            b = input("")

            if b == 'f':
                Enviar(channel,"O Aluno saiu da conversa.")
                Sair(connection)
                print(" ### Voce saiu da conversa ### ")
                break
            else:
                Enviar(channel, b)


                


# criando thread
servidor = TH_server(1)
servidor.start()

envio = TH_send(1)
envio.start()

