from redis.asyncio import Redis

from database.databases import get_redis


class RedisClientService:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self.key = "last_upadate"

    async def _check_key(
        self, date_timestamp: int, redis_value: int, redis_client: Redis
    ) -> bool:
        if date_timestamp == int(redis_value):
            return False
        if date_timestamp > int(redis_value):
            await redis_client.set(self.key, date_timestamp)
            return True

    async def check_last_date(self, date_timestamp: int) -> bool:
        async with get_redis() as redis_client:
            if found_key := await redis_client.get(self.key):
                return await self._check_key(
                    date_timestamp=date_timestamp,
                    redis_value=found_key,
                    redis_client=redis_client,
                )

            lock_key = f"{self.key}:lock"
            async with redis_client.lock(
                lock_key, timeout=10, blocking_timeout=15
            ):
                if found_key := await redis_client.get(self.key):
                    return await self._check_key(
                        date_timestamp=date_timestamp, redis_value=found_key
                    )

            await redis_client.set(self.key, date_timestamp)
            return True
