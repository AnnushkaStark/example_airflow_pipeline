from contextlib import asynccontextmanager
from typing import AsyncIterator

from asynch import Connection
from asynch import errors
from redis.asyncio import Redis

from config.configs import click_house_settings
from config.configs import redis_settings
from sql.create_table import init_query
from utils.errors import ClichkhouseError


@asynccontextmanager
async def get_redis() -> AsyncIterator[Redis]:
    redis_client = Redis.from_url(redis_settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.close()


async def get_clickhuose_conn() -> AsyncIterator[Connection]:
    conn = Connection(
        database=click_house_settings.CLICKHOUSE_DB,
        host=click_house_settings.CLICKHOUSE_HOST,
        port=click_house_settings.CLICHOUSE_PORT,
        user=click_house_settings.CLICKHOUSE_USER,
        password=click_house_settings.CLICKHOUSE_PASSWORD,
    )
    async with conn.cursor() as cursor:
        try:
            await cursor.execute(init_query)
            yield conn
        except errors.ClickHouseException as err:
            raise ClichkhouseError from err
        finally:
            conn.close()
