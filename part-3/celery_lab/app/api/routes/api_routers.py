from celery.result import AsyncResult
from fastapi import APIRouter

from app.celery.tasks import make_api_request_weather, make_api_request_event

router = APIRouter(tags=["api"], prefix='/api')

@router.get("/weather/")
async def get_weather_by_city(city: str):
    """
    Get the weather for a given city.
    
    This endpoint will trigger a Celery task to make an API request to WeatherAPI
    to retrieve the current weather for the given city.
    
    The task ID will be returned in the response.
    
    Parameters:
    - city: str
        The city for which to retrieve the weather.
    
    Returns:
    - task_id: str
        The ID of the Celery task.
    """
    task = make_api_request_weather.delay(
        json_data={'q': city}
    )
    return {"task_id": task.id}


@router.get("/event/")
async def get_events_by_city(city: str):
    """
    Get the events for a given city.
    
    This endpoint will trigger a Celery task to make an API request to Ticketmaster API
    to retrieve the events for the given city.
    
    The task ID will be returned in the response.
    
    Parameters:
    - city: str
        The city for which to retrieve the events.
    
    Returns:
    - task_id: str
        The ID of the Celery task.
    """
    task = make_api_request_event.delay(
        json_data={'city': city}
    )
    return {"task_id": task.id}


@router.get("/task/{task_id}")
async def get_task_result(task_id: str):
    """
    Get the result of a Celery task.

    This endpoint will retrieve the result of a Celery task with the given task ID.
    """
    task_result = AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.successful():
        result["result"] = task_result.result
    elif task_result.failed():
        result["error"] = str(task_result.result)

    return result
