from abc import ABC, abstractmethod
import logging
import functools
from broker_connection import RabbitMqConnection
from vault_helper import VaultHelper
import json
import requests
from pathlib import Path

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class BaseConsumer(ABC):
    def __init__(self, connection: RabbitMqConnection, queue_name):
        self._connection = connection
        self._channel = connection.channel
        self._consuming = False
        self._consumer_tag = None
        self._queue_name = queue_name

    def start_consuming(self):
        if not self._connection.ready:
            raise RuntimeError("RabbitMQ connection is not ready")

        LOGGER.info('Starting consumer for queue: %s', self._queue_name)

        self._channel.basic_qos(prefetch_count=1)
        self._consumer_tag = self._channel.basic_consume(
            self._queue_name,
            self.on_message,
            auto_ack=False
        )

        self._consuming = True

        LOGGER.info('Consumer started with tag: %s', self._consumer_tag)

    @abstractmethod
    def on_message(self, _unused_channel, basic_deliver, properties, body):
        pass

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, callback=cb)

    def on_cancelok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)
        """
        self._consuming = False

        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOGGER.info('Closing the channel')
        self._channel.close()

    @property
    def is_consuming(self):
        return self._consuming


class ApiConsumer(BaseConsumer, ABC):
    def __init__(self, connection: RabbitMqConnection, queue_name, vault_helper: VaultHelper, api_key):
        """
        Initialize the ApiConsumer instance.

        :param connection: RabbitMqConnection
            The RabbitMQ connection object.
        :param queue_name: str
            The name of the queue to consume from.
        :param vault_helper: VaultHelper
            The Vault helper object.
        :param api_key: str
            The API key to fetch from Vault.
        """
        super().__init__(connection, queue_name)
        self._vault_helper = vault_helper
        self._api_key = api_key

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)

        json_data = json.loads(body)
        api_key = self._vault_helper.get_api_key(alias=self._api_key)

        LOGGER.info('API key: %s', api_key)
        LOGGER.info('Json data for %s: %s', self.__class__.__name__, json_data)

        response = self.make_api_request(api_key, json_data)

        self.save_response(response)
        LOGGER.debug('Response: %s', response.json())

        self.acknowledge_message(basic_deliver.delivery_tag)

    @abstractmethod
    def make_api_request(self, api_key: str, json_data: dict) -> requests.Response:
        pass

    def save_response(self, response: requests.Response):
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)

        filename = data_dir / f"{self.__class__.__name__.lower().replace('consumer', '')}_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)


class WeatherConsumer(ApiConsumer):

    def make_api_request(self, api_key: str, json_data: dict) -> requests.Response:
        """
        Make an API request to WeatherAPI.

        :param str api_key: The API key to use for the request
        :param dict json_data: The JSON data to use for the request
        :return: The response from the API
        :rtype: requests.Response
        """
        return requests.get(
            url='http://api.weatherapi.com/v1/current.json',
            params={
                'key': api_key,
                'q': json_data.get('q')
            }
        )


class EventConsumer(ApiConsumer):

    def make_api_request(self, api_key: str, json_data: dict) -> requests.Response:
        """
        Make a GET request to the Ticketmaster API to retrieve events for a given city.

        :param str api_key: The API key to use for the request
        :param dict json_data: The JSON data to use for the request
        :return: The response from the API
        :rtype: requests.Response
        """
        return requests.get(
            url='https://app.ticketmaster.com/discovery/v2/events.json',
            params={
                'apikey': api_key,
                'city': json_data.get('city')
            }
        )
