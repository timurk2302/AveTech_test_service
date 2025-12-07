from typing import Annotated
from fastapi import Depends
from app.service.redis_client import redis_client
import redis.asyncio as redis

async def get_redis_client() -> redis.Redis:
    """
    Зависимость для получения клиента Redis
    :return: redis.Redis
    """
    return await redis_client.get_client()  

RedisDependency = Annotated[redis.Redis, Depends(get_redis_client)]