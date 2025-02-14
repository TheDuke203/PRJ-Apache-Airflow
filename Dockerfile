FROM apache/airflow:2.10.5-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

USER airflow

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt