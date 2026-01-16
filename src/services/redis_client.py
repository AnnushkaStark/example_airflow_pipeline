import logging

from redis.asyncio import Redis

from database.databases import get_redis

logger = logging.getLogger("RedisClientService")


class RedisClientService:
    def __init__(self, ttl: int = 1440):
        self.ttl = ttl
        self.key = "last_upadate"

    async def _check_key(
        self, date_timestamp: int, redis_value: int, redis_client: Redis
    ) -> bool:
        logger.info("Проверка последнeго обновлния")
        if date_timestamp == int(redis_value):
            logger.info("Данные не обновились с последенего запроса")
            return False

        if date_timestamp > int(redis_value):
            logger.info("Получено обновление курсов валют")
            await redis_client.set(self.key, date_timestamp)
            return True

        return False

    async def check_last_date(self, date_timestamp: int) -> bool:
        logger.info("Проверка наличия последнего обновления")
        async with get_redis() as redis_client:
            if found_key := await redis_client.get(self.key):
                logger.info("Ключ последнего обновления найден")
                return await self._check_key(
                    date_timestamp=date_timestamp,
                    redis_value=found_key,
                    redis_client=redis_client,
                )

            logger.info("Проверка наличия последнего обновления с блокировкой")
            lock_key = f"{self.key}:lock"
            async with redis_client.lock(
                lock_key, timeout=10, blocking_timeout=15
            ):
                if found_key := await redis_client.get(self.key):
                    logger.info(
                        "Ключ последнего обновления найден после блокировки"
                    )
                    return await self._check_key(
                        date_timestamp=date_timestamp, redis_value=found_key
                    )

            logger.info("Запись таймстампа поседнего обновления")
            await redis_client.set(self.key, date_timestamp)
            return True
