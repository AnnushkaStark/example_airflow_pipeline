#!/bin/bash
set -e

echo "Waiting for Postgres..."
while ! nc -z airflow_db 5432; do
  sleep 1
done
echo "Postgres is up!"

airflow db migrate


echo "Creating admin user..."
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin || echo "Admin already exists."

echo "Starting Scheduler and Webserver..."
airflow scheduler & 
exec airflow webserver

