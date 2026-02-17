import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    dag_id="dbt_snowflake_pipeline",
    start_date=datetime(2025,1,1),
    schedule="@daily",
    catchup=False,
) as dag:

    dbt_run = DockerOperator(
        task_id="dbt_run",
        image="dbt-snowflake:latest",
        command="run --project-dir /opt/dbt --profiles-dir /root/.dbt",
        auto_remove=True,
        environment={
            "SNOWFLAKE_ACCOUNT": os.getenv("SNOWFLAKE_ACCOUNT"),
            "SNOWFLAKE_DBT_USER": os.getenv("SNOWFLAKE_DBT_USER"),
            "SNOWFLAKE_DBT_PASSWORD": os.getenv("SNOWFLAKE_DBT_PASSWORD"),
            "SNOWFLAKE_DBT_ROLE": os.getenv("SNOWFLAKE_DBT_ROLE"),
            "SNOWFLAKE_WAREHOUSE": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "SNOWFLAKE_DATABASE": "BANKING",
            "SNOWFLAKE_SCHEMA": "ANALYTIC"
        },
        docker_url="unix://var/run/docker.sock",
        network_mode="banking-mds-net",
        mount_tmp_dir=False,
    )

    dbt_test = DockerOperator(
        task_id="dbt_test",
        image="dbt-snowflake:latest",
        command="test --project-dir /opt/dbt --profiles-dir /root/.dbt",
        auto_remove=True,
        environment={
            "SNOWFLAKE_ACCOUNT": os.getenv("SNOWFLAKE_ACCOUNT"),
            "SNOWFLAKE_DBT_USER": os.getenv("SNOWFLAKE_DBT_USER"),
            "SNOWFLAKE_DBT_PASSWORD": os.getenv("SNOWFLAKE_DBT_PASSWORD"),
            "SNOWFLAKE_DBT_ROLE": os.getenv("SNOWFLAKE_DBT_ROLE"),
            "SNOWFLAKE_WAREHOUSE": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "SNOWFLAKE_DATABASE": "BANKING",
            "SNOWFLAKE_SCHEMA": "ANALYTIC"
        },
        docker_url="unix://var/run/docker.sock",
        network_mode="banking-mds-net",
        mount_tmp_dir=False,
    )

    dbt_run >> dbt_test
