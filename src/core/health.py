from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from fastapi.responses import JSONResponse
from fastapi import status

from src.db.connection import engine


async def health() -> dict | JSONResponse:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"details": "connection closed"},
        )
    return {
        "status": "ok",
        "database": "ok",
        }