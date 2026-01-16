#!/bin/bash


echo Waiting_for_Postgres
while ! nc -z airflow_db 5432; do
  sleep 1
done
echo Postgres_is_up

echo Running_Migrations
airflow db migrate

echo Creating_Admin
#airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin || echo Admin_exists

echo Starting_Airflow
airflow scheduler &
airflow dag-processor &
exec airflow api-server
