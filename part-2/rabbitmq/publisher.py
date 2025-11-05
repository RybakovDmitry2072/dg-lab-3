import logging
from broker_connection import RabbitMqConnection
import pika
import json

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class TaskPublisher:
    ROUTING_KEY_FOR_WEATHER = 'task.weather'
    ROUTING_KEY_FOR_EVENTS = 'task.events'
    EXCHANGE = 'task.exchange'

    def __init__(self, connection: RabbitMqConnection):
        self._connection = connection
        self.__setup_delivery_confirmation()

    def __setup_delivery_confirmation(self):
        """
        Setup delivery confirmation callback.

        This method adds the delivery confirmation callback to the
        channel. When a message is confirmed or rejected by RabbitMQ,
        the __on_delivery_confirmation method will be called with a
        pika.frame.Method object as an argument. The method object
        contains information about whether the message was confirmed or
        rejected.
        """
        self._connection.channel.confirm_delivery(self.__on_delivery_confirmation)

    def __on_delivery_confirmation(self, method_frame):
        """
        Called when a message is confirmed or rejected by RabbitMQ.

        :param pika.frame.Method method_frame: The Basic.Ack or Basic.Nack frame

        This method is a callback that is added to the channel using the
        add_on_delivery_confirmation_callback method. When a message is confirmed
        or rejected by RabbitMQ, this method is called with a
        pika.frame.Method object as an argument. The method object
        contains information about whether the message was confirmed or
        rejected.
        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        if confirmation_type == 'ack':
            LOGGER.debug("Message confirmed")
        else:
            LOGGER.warning("Message rejected")

    def publish_weather_task(self, city):
        """
        Publish a weather task for a given city.

        :param str city: The city for which the weather task should be published
        """
        channel = self._connection.channel
        properties = pika.BasicProperties(app_id='example-publisher',
                                          content_type='application/json')

        channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY_FOR_WEATHER,
                              json.dumps({'task_type': 'weather', 'q': city},
                                         ensure_ascii=False),
                              properties)

        LOGGER.info('Published weather task for %s', city)

    def publish_events_task(self, city):
        """
        Publish an events task for a given city.

        :param str city: The city for which the events task should be published
        """
        channel = self._connection.channel
        properties = pika.BasicProperties(app_id='example-publisher',
                                          content_type='application/json')

        channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY_FOR_EVENTS,
                              json.dumps({'task_type': 'events', 'city': city},
                                         ensure_ascii=False),
                              properties)

        LOGGER.info('Published events task for %s', city)
