import asyncio
from datetime import datetime
from datetime import timedelta

from airflow.sdk import dag, task 

from services.clickhouse_client import ClickHouseService
from services.currency_parser import CurrencyParserService
from services.etl import EtlService
from services.httpx_client import HttpxClientService
from services.producer import ProducerService
from services.redis_client import RedisClientService


@task(task_id="etl_process_daily")
def run_etl():
    etl = EtlService(
        api_client=HttpxClientService(),
        parser=CurrencyParserService(),
        redis_client=RedisClientService(),
        producer=ProducerService(),
        clickhouse_client=ClickHouseService(),
    )
    asyncio.run(etl.start_etl_executor())
    return "Ok"


default_args = {
    "owner": "AirflowExample",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="example_etl_v3",
    schedule="@daily",
    start_date=datetime(2026, 1, 12),
    catchup=False,
    tags=["airflow_3_sdk"],
    default_args=default_args
)
def my_etl_dag():
    run_etl()


my_etl_dag()
