# Фикстуры - функции, которые подготавливают тестовое окружение, 
# создают данные или объекты, выполняют очистку ресурсов после завершения тестов.


# имитирует HTTP-вызовы внутри оперативной памяти. 
# Клиент берет ваш запрос (client.get("/users")), 
# напрямую передает его в код app (FastAPI) и возвращает ответ. 

# В тестах вам не нужно писать полный адрес, достаточно 
# указать эндпоинт: await client.get("/v1/users"). 
# Клиент сам превратит это в http://test/v1/users и передаст в FastAPI.

# Если какой-то тест попросит аргумент с именем client, то создастся он по этим правилам:


import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.main import app
from src.db.context import get_db


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db_test"
)


engine = create_async_engine(url=TEST_DATABASE_URL)


TestAsyncSesMaker = async_sessionmaker(
    engine, 
    autoflush=False, 
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db_session():
    async with TestAsyncSesMaker() as session:
        try:
            yield session
        finally:
            await session.rollback() # исключение не нужно, оно само поднимется в yield


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


    app.dependency_overrides.clear()