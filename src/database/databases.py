from contextlib import asynccontextmanager
from typing import AsyncIterator
from redis.asyncio import Redis

from config.configs import click_house_settings
from config.configs import redis_settings
import clickhouse_connect
from sql import create_table


@asynccontextmanager
async def get_redis() -> AsyncIterator[Redis]:
    redis_client = Redis.from_url(redis_settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.close()


@asynccontextmanager
async def get_clickhouse_conn():
    conn = await clickhouse_connect.get_async_client(
        database=click_house_settings.CLICKHOUSE_DB,
        host=click_house_settings.CLICKHOUSE_HOST,
        port=click_house_settings.CLICKHOUSE_PORT,
        user=click_house_settings.CLICKHOUSE_USER,
        password=click_house_settings.CLICKHOUSE_PASSWORD,
    )
    await conn.command(f"USE {click_house_settings.CLICKHOUSE_DB}")
    await conn.command(create_table.init_query)
    yield conn
