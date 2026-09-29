from maxapi import Bot
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis.asyncio as redis


class Settings(BaseSettings):

    # MAX
    MAX_BOT_TOKEN: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)


bot = Bot(
    token=settings.MAX_BOT_TOKEN
)