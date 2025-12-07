FROM apache/airflow:2.11.0rc1-python3.9

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        curl \
        libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow


COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt


COPY dags/ /opt/airflow/dags/