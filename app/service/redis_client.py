import redis.asyncio as redis
from app.config import settings

class RedisClient:
    """
    Клиент для работы с Redis
    """
    def __init__(self):
        self.redis_client = None

    
    async def connect(self):
        """
        Подключение к Redis
        """
        self.redis_client = await redis.from_url(
            f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True,
        )

    async def disconnect(self):
        """
        Отключение от Redis
        """
        await self.redis_client.aclose()

    async def get_client(self)-> redis.Redis:
        """
        Получение клиента Redis
        :return: redis.Redis
        """
        if not self.redis_client:
            await self.__connect()
        return self.redis_client

redis_client = RedisClient()
