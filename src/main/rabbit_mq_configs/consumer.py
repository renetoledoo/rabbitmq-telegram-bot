import os
import pika
import json
from dotenv import load_dotenv

load_dotenv()

def rabbitmq_callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    msg_dump = json.loads(msg)
    msg_clean = msg_dump.get("msg", "Não encontrado")
    print("Mensagem recebida:", msg_clean)


class RabbitMQConsumer: 
    
    def __init__(self, queue: str) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = int(os.getenv("RABBITMQ_PORT"))
        self.__username = os.getenv("RABBITMQ_USERNAME")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__queue = queue
        self.__routing_key = os.getenv("RABBITMQ_ROUTING_KEY", None)
        self.__channel  = self.create_channel()

    def create_channel(self) -> None:
        # https://www.rabbitmq.com/tutorials/tutorial-one-python
        connection_parameters = pika.ConnectionParameters(
            host= self.__host,
            port=self.__port,
            credentials= pika.PlainCredentials(username=self.__username, password=self.__password)
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )

        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback= rabbitmq_callback
        )
        return channel
    
    def start(self):
        print('[!]- Sistem Conectado ao RabbitMQ.')
        self.__channel.start_consuming()