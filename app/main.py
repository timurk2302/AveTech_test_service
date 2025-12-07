from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.endpoints import phone_address_router
from app.service.redis_client import redis_client
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Запуск
    await redis_client.connect()
    print(f"Connected to Redis at {settings.redis_host}:{settings.redis_port}")
    
    yield
    
    # Остановка
    await redis_client.disconnect()
    print("Disconnected from Redis")


app = FastAPI(
    title=settings.app_name,
    description="Микросервис для хранения и управления связками 'телефон-адрес'",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Регистрация роутеров
app.include_router(
    phone_address_router,
    prefix="/api/v1/phones",
    tags=["phone-address"],
)