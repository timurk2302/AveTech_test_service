from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Настройки для приложения
    """
    app_name: str = "FastAPI Application"
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ttl: int = 86400 # 24 часа

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()