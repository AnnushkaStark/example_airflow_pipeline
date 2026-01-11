import json
import logging
from typing import Any
from typing import Dict
from typing import List

from aiokafka import AIOKafkaProducer

from config.configs import kafka_settings

logger = logging.getLogger("ProducerService")


class ProducerService:
    def __init__(self):
        self.bootstrap_url = kafka_settings.BOOTSTRAP_URL
        self.topic = kafka_settings.TOPIC
        self.producer = None

    async def start(self) -> None:
        logger.info("Инициализация продюссера")
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_url,
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        logger.info("Продюссер запущен")
        await self.producer.start()

    async def stop(self) -> None:
        logger.info("Остановка продюссера")
        if self.producer:
            logger.info("Продюссер остановлен")
            await self.producer.stop()

    async def push_rates(self, rates_list: List[Dict[str, Any]]):
        logger.info("Отправка информации о курсах валют в топик Kafka")

        if not self.producer:
            await self.start()

        for rate_data in rates_list:
            logger.info("Определение ключа партиции")
            partition_key = rate_data["currency_code"][0]
            await self.producer.send_and_wait(
                self.topic, key=partition_key, value=rate_data
            )
            logger.info("Сообщение отправлено")
