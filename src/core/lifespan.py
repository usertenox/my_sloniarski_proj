from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.connection import close_db_connections 

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await close_db_connections()