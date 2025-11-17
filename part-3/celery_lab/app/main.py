from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import create_db_and_tables, engine
from .api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield

    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
