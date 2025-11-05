from broker_connection import RabbitMqConnection


class RabbitMQInitializer:

    def __init__(self, connection: RabbitMqConnection, queues, exchange):
        """
        Initialize the RabbitMQInitializer object.

        :param connection: RabbitMqConnection: The RabbitMQ connection object
        :param list queues: The list of queues to declare
        :param str exchange: The name of the exchange to declare
        """
        self._connection = connection
        self._channel = connection.channel
        self._queues = queues
        self._exchange = exchange

    def init(self):
        """
        Initialize RabbitMQ by declaring the exchange and queues.

        :raises RuntimeError: If RabbitMQ connection is not ready
        """
        if not self._connection.ready:
            raise RuntimeError('RabbitMQ connection must be established')

        self._connection.channel.exchange_declare(exchange=self._exchange,
                                                  exchange_type='direct',
                                                  durable=True)
        for queue in self._queues:
            routing_key = f'task.{queue}'
            self._channel.queue_declare(queue=queue)
            self._channel.queue_bind(exchange=self._exchange, queue=queue, routing_key=routing_key)
