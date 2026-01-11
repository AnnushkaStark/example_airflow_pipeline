import logging
from typing import Any
from typing import Dict
from typing import List

from database.databases import get_clickhuose_conn
from sql.insert import insert_query

logger = logging.getLogger("ClickHouseService")


class ClickHouseService:
    async def insert_rates_dict(
        self, rates_dicts: List[Dict[str, Any]]
    ) -> None:
        logger.info("Сохранение данных о курсах валют")
        async with get_clickhuose_conn() as conn:
            cursor = conn.cursor()
            await cursor.executemany(insert_query, rates_dicts)
            logger.info("Данные сохранены")
            await conn.сlose()
