from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis.asyncio import Redis

from config.configs import redis_settings


@asynccontextmanager
async def get_redis() -> AsyncIterator[Redis]:
    redis_client = Redis.from_url(redis_settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.close()
