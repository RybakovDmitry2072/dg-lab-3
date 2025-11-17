"""
This file contains the configuration for Celery.

It imports the build_broker_url function from the utils module to
construct the broker URL from environment variables.

The Celery configuration is defined as a dictionary with the
following keys:
- broker_url: the URL of the RabbitMQ broker
- result_backend: the backend used for storing the results of tasks
- imports: a list of modules to import when the Celery worker starts

The values of these keys are set to the appropriate values for the
Celery lab application.
"""

from app.utils.connection_builder import build_broker_url, build_engine_url

broker_url = build_broker_url()
result_backend = build_engine_url(prefix='db+postgresql+psycopg2')
imports = ('app.celery.tasks',)

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True
