from fastapi import APIRouter

from .routes import api_routers

api_router = APIRouter()
api_router.include_router(api_routers.router)
