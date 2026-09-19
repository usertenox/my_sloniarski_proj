from fastapi import FastAPI

from src.api.v1.router import api_router
from src.core.config import settings
from src.core.lifespan import lifespan
from src.utils.exception_handlers import register_error_handlers
from src.core.health import health

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version="1.0.1",
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(api_router)
register_error_handlers(app)

# FastAPI (наследует APIRouter)
# APIRouter — класс, который отвечает за сбор и группировку маршрутов. Именно в нем физически объявлен метод .get()
# APIRoute — объект конкретного маршрута. Когда декоратор срабатывает, он создает экземпляр этого класса для вашего /health.
# привязываем путь к функции в словаре маршрутов get'а

@app.get("/health")
async def get_health():
    return await health()