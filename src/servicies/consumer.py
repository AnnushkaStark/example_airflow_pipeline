import json
import logging

from aiokafka import AIOKafkaConsumer

from config.configs import kafka_settings
from servicies.clickhouse_client import ClickHouseService

logger = logging.getLogger("ConsumerService")


class ConsumerService:
    def __init__(
        self, clichkouse_service: ClickHouseService, batch_size: int = 1000
    ):
        self.batch_size = batch_size
        self.cklichouse_service = clichkouse_service

    async def _consumer_init(self) -> None:
        logger.info("Запуск консьюмера")
        self.consumer = AIOKafkaConsumer(
            kafka_settings.TOPIC,
            bootstrap_servers=kafka_settings.BOOTSTRAP_URL,
            group_id="courency_group",
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        logger.info("Консьюмер запущен")

    async def read_messages(self):
        consumer = await self._consumer_init()
        logger.info("Получение группы сообщений")

        data_map = await self.consumer.getmany(
            timeout_ms=1000, max_records=self.batch_size
        )

        batch = []
        for messages in data_map.values():
            for msg in messages:
                batch.append(json.loads(msg.value))

        if batch:
            await self.cklichouse_service.insert_rates_dict(batch)
            logger.info(f"Получено {len(batch)} записей ")

        await consumer.stop()
        logger.info("Воркер остановлен")
