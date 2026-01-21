import logging
from typing import Any
from typing import Dict
from typing import List

from config.configs import click_house_settings
from database.databases import get_clickhouse_conn
from sql.insert import insert_query

logger = logging.getLogger("ClickHouseService")


class ClickHouseService:
    def __init__(self):
        self.rates_columns = ["currency_code", "rate", "api_timestamp"]

    async def insert_rates_dict(
        self, rates_dicts: List[Dict[str, Any]]
    ) -> None:
        logger.info("Сохранение данных о курсах валют")
        async with get_clickhouse_conn() as conn:
            data = [
                (d["currency_code"], float(d["rate"]), d["api_timestamp"])
                for d in rates_dicts
            ]

            await conn.command(data=data, cmd=insert_query)
            logger.info("Данные сохранены")
