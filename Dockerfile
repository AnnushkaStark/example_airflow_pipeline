FROM apache/airflow:3.1.5

USER root
RUN apt-get update && apt-get install -y build-essential && apt-get clean

USER airflow


COPY requirements.txt /opt/airflow/requirements.txt


RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt


COPY airflow_user.sh /airflow_user.sh

USER root

RUN chmod +x /airflow_user.sh

USER airflow

ENTRYPOINT ["/airflow_user.sh"]