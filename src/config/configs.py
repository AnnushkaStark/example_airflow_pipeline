from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class ClickHouseSettings(BaseSetting):
    CLICKHOUSE_HOST: str
    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: int = 1


class KafkaSettings(BaseSetting):
    BOOTSTRAP_URL: str = "kafka:29092"
    TOPIC: str


class ReddisSettings(BaseSetting):
    HOST: str = "redis"
    PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"


class HttpxClientSesttings(BaseSetting):
    ROOT_URL: str
    API_KEY: str


click_house_settings = ClickHouseSettings()
kafka_settings = KafkaSettings()
redis_settings = ReddisSettings()
httpx_client_settings = HttpxClientSesttings()
