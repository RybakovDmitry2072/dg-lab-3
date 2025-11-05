from vault_helper import VaultHelper
from broker_connection import RabbitMqConnection
from initializer import RabbitMQInitializer
from publisher import TaskPublisher
from concumers import WeatherConsumer, EventConsumer
import functools

def on_connection_ready(connection, vault_helper):
    queues = ['weather', 'events']
    exchange = 'task.exchange'

    initializer = RabbitMQInitializer(connection,
                                      queues=queues,
                                      exchange=exchange)
    initializer.init()

    publisher = TaskPublisher(connection)
    publisher.publish_weather_task('Paris')
    publisher.publish_events_task('Paris')

    api_key_alias_for_weather = 'weather-api-key'
    api_key_alias_for_events = 'events-api-key'
    event_consumer = EventConsumer(connection, queues[1], vault_helper, api_key_alias_for_events)
    event_consumer.start_consuming()

    weather_consumer = WeatherConsumer(connection, queues[0], vault_helper, api_key_alias_for_weather)
    weather_consumer.start_consuming()

def main():
    vault_helper = VaultHelper()
    rabbitmq_credentials = vault_helper.get_rabbitmq_credentials()

    amqp_url = f'amqp://{rabbitmq_credentials["username"]}:{rabbitmq_credentials["password"]}@localhost:5672/%2F'

    cb = functools.partial(on_connection_ready, vault_helper=vault_helper)
    connection = RabbitMqConnection(amqp_url, on_ready_callback=cb)

    connection.run()

if __name__ == '__main__':
    main()
