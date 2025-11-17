from typing import Any

import requests

from app.core.config import settings
from .celery_app import celery_app


@celery_app.task()
def make_api_request_weather(json_data: dict) -> dict[str, Any]:
    """
    Make an API request to WeatherAPI.

    :param str api_key: The API key to use for the request
    :param dict json_data: The JSON data to use for the request
    :return: The response from the API
    :rtype: dict[str, Any]
    """
    return requests.get(
        url='http://api.weatherapi.com/v1/current.json',
        params={
            'key': settings.api_key_for_weather,
            **json_data
        }
    ).json()


@celery_app.task()
def make_api_request_event(json_data: dict) -> dict[str, Any]:
    """
    Make a GET request to the Ticketmaster API to retrieve events for a given city.

    :param str api_key: The API key to use for the request
    :param dict json_data: The JSON data to use for the request
    :return: The response from the API
    :rtype: dict[str, Any]
    """
    return requests.get(
        url='https://app.ticketmaster.com/discovery/v2/events.json',
        params={
            'apikey': settings.api_key_for_event,
            **json_data
        }
    ).json()
