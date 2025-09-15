import pika
import os
import json
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env 
load_dotenv()

class RabbitMQPublisher: 
    
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = int(os.getenv("RABBITMQ_PORT"))
        self.__username = os.getenv("RABBITMQ_USERNAME")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__exchange = os.getenv("RABBITMQ_EXCHANGE")
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
        return channel
    
    def send_message(self, body: dict):
        # https://www.rabbitmq.com/tutorials/tutorial-three-python
        self.__channel.basic_publish(exchange= self.__exchange,
                    routing_key= self.__routing_key,
                    body= json.dumps(body),
                    properties = pika.BasicProperties(
                        delivery_mode=2
                    )
        )
        print('[+] Mensagem enviada.')
    
    

rabbit_mq_publisher = RabbitMQPublisher()
rabbit_mq_publisher.send_message({'msg': 'Estou no publisher'})