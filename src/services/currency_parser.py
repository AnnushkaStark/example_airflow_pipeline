import logging
from typing import Any
from typing import Dict
from typing import List

logger = logging.getLogger("CurrencyParser")


class CurrencyParser:
    def _get_api_timestamp(self, data: Dict[str, str]) -> int:
        logger.info("Получение последней даты обновлнения курса")
        return data.get("time_last_update_unix")

    def _get_currency_dump_by_name(
        self,
        last_update: int,
        name: str,
        rate: float,
    ) -> Dict[str, Any]:
        logger.info("Формирование сообщение для продюссера")
        return {
            "time_last_update_unix": last_update,
            "currency_code": name,
            "rate": rate,
        }

    def get_currency_dumps(self, data: Dict[str, str]) -> List[Dict[str, Any]]:
        logger.info("Получение списка сообщений для каждой валюты")
        res = []
        last_update = self._get_api_timestamp(data=data)
        currency_dict = data.get("conversion_rates")
        for key, value in currency_dict.items():
            dct = self._get_currency_dump_by_name(
                last_update=last_update,
                name=key,
                rate=value,
            )
            res.append(dct)
        return res
