import logging
from typing import Any
from typing import Dict
from typing import List

from config.configs import click_house_settings
from database.databases import get_clickhouse_conn

logger = logging.getLogger("ClickHouseService")


class ClickHouseService:
    def __init__(self):
        self.rates_columns = ["currency_code", "rate", "api_timestamp"]

    async def insert_rates_dict(
        self, rates_dicts: List[Dict[str, Any]]
    ) -> None:
        logger.info(f"Сохранение данных о курсах валют")
        async with get_clickhouse_conn() as conn:
            #data_to_insert = [d.values() for d in rates_dicts]
            await conn.insert(
                table="currency_rates",
                data=[tuple(d.values()) for d in rates_dicts],
                database=click_house_settings.CLICKHOUSE_DB,
                column_names=self.rates_columns,
                column_oriented=False,
                column_type_names=["String", 'Float64', 'DateTime'] 
            )
            logger.info("Данные сохранены")
