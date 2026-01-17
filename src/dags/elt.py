import asyncio
from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from services.clickhouse_client import ClickHouseService
from services.currency_parser import CurrencyParserService
from services.elt import EltService
from services.httpx_client import HttpxClientService
from services.producer import ProducerService
from services.redis_client import RedisClientService


def run_elt():
    elt = EltService(
        api_client=HttpxClientService(),
        parser=CurrencyParserService(),
        redis_client=RedisClientService(),
        producer=ProducerService(),
        clickhouse_client=ClickHouseService(),
    )
    asyncio.run(elt.start_elt_executor())


default_args = {
    "owner": "AirflowExample",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="exapmle_elt_v1",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 12),
    catchup=False,
    tags=["airflow_example"],
) as dag:
    task_execute_elt = PythonOperator(
        task_id="elt_process_daily", python_callable=run_elt
    )
