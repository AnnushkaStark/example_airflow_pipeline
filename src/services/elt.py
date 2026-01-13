from services.clickhouse_client import ClickHouseService
from services.consumer import ConsumerService
from services.currency_parser import CurrencyParserService
from services.httpx_client import HttpxClientService
from services.producer import ProducerService
from services.redis_client import RedisClientService


class EltService:
    def __init__(
        self,
        api_client: HttpxClientService,
        parser: CurrencyParserService,
        redis_client: RedisClientService,
        producer: ProducerService,
        clickhouse_client: ClickHouseService,
    ):
        self.api_client = api_client
        self.parser = parser
        self.redis_client = redis_client
        self.producer = producer
        self.clickhouse_client = clickhouse_client
        self.consumer = None

    async def start_elt_executor(self) -> None:
        response_data = await self.api_client.get_currency_rates()
        if await self.redis_client.check_last_date(
            date_timestamp=self.parser._get_api_timestamp(data=response_data)
        ):
            await self.producer.push_rates(
                rates_list=self.parser.get_currency_dumps(data=response_data)
            )
            self.consumer = ConsumerService(
                clichkouse_service=self.clickhouse_client
            )
            await self.consumer.read_messages()
