FROM apache/airflow:2.9.3

USER airflow

RUN pip install --no-cache-dir dbt-core dbt-snowflake