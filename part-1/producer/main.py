import pika
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    credentials = pika.PlainCredentials(
        username=os.getenv('username'),
        password=os.getenv('password')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()