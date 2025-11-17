import os

# from dotenv import load_dotenv


def build_broker_url():
    """
    Build a broker URL from environment variables.

    The following environment variables are required:
    - BROKER_HOST: the hostname or IP address of the RabbitMQ broker
    - BROKER_PORT: the port number of the RabbitMQ broker
    - BROKER_USERNAME: the username to use when connecting to the RabbitMQ broker
    - BROKER_PASSWORD: the password to use when connecting to the RabbitMQ broker

    Returns:
        str: the broker URL in the format amqp://username:password@hostname:port/
    """
    # load_dotenv()
    broker_host = os.getenv('BROKER_HOST')
    broker_port = os.getenv('BROKER_PORT')
    broker_username = os.getenv('BROKER_USERNAME')
    broker_password = os.getenv('BROKER_PASSWORD')
    return f"amqp://{broker_username}:{broker_password}@{broker_host}:{broker_port}/"


def build_engine_url(prefix="postgresql+psycopg2"):
    """
    Build a database engine URL from environment variables.

    The following environment variables are required:
    - ENGINE_HOST: the hostname or IP address of the database engine
    - ENGINE_PORT: the port number of the database engine
    - ENGINE_NAME: the name of the database
    - ENGINE_USERNAME: the username to use when connecting to the database engine
    - ENGINE_PASSWORD: the password to use when connecting to the database engine

    Returns:
        str: the database engine URL in the format postgresql+psycopg2://username:password@hostname:port/dbname
    """
    # load_dotenv()
    engine_host = os.getenv('ENGINE_HOST')
    engine_port = os.getenv('ENGINE_PORT')
    engine_name = os.getenv("ENGINE_NAME")
    engine_username = os.getenv('ENGINE_USERNAME')
    engine_password = os.getenv('ENGINE_PASSWORD')
    return f"{prefix}://{engine_username}:{engine_password}@{engine_host}:{engine_port}/{engine_name}"
