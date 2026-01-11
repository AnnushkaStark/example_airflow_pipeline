from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent



class ClickHouseSettings(BaseSetting):
    pass



class KafkaSettings(BaseSetting):
    pass


class ReddisSettings(BaseSetting):
    HOST: str = "redis"
    PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"


class HttpxClientSesttings(BaseSetting):
    ROOT_URL: str
    API_KEY: str


redis_settings = ReddisSettings()
httpx_client_settings = HttpxClientSesttings()
