FROM apache/airflow:2.10.3

RUN pip install apache-airflow-providers-airbyte psycopg2-binary python-dotenv