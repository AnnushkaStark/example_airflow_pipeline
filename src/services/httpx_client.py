import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from typing import Dict

from httpx import AsyncClient

from config.configs import httpx_client_settings
from utils.errors import HttpxClientError

logger = logging.getLogger("HttpxClentService")


class HttpxClientService:
    @asynccontextmanager
    async def _get_client(self) -> AsyncIterator[AsyncClient]:
        client = AsyncClient(base_url=httpx_client_settings.ROOT_URL)
        yield client

    async def get_currency_rates(self) -> Dict[str, str]:
        logger.info("Получение информации о курсах валют")
        async with self._get_client() as client:
            response = await client.get(
                f"/{httpx_client_settings.API_KEY}/latest/USD"
            )

            if response.status_code != 200:
                response_data = response.json()
                logger.error(
                    f"Ошибка получения информации о курсах валют {response.status_code}, {response_data}"
                )
                raise HttpxClientError(
                    f"Ошибка получения информации о курсах валют {response.status_code}, {response_data}"
                )
            logger.info("Получены данные о курсах валют")
            return response.json()
