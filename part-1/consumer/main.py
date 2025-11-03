import pika
import os
from dotenv import load_dotenv

load_dotenv()


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def main():
    credentials = pika.PlainCredentials(
        username=os.getenv('username'),
        password=os.getenv("password")
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello',
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    main()
