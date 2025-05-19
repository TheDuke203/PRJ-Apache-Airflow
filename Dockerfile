FROM apache/airflow:2.11.0rc1-python3.9
USER root

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get -y install libgomp1

USER airflow

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt