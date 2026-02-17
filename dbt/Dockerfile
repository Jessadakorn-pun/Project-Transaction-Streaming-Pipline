FROM python:3.11-slim

WORKDIR /opt/dbt

COPY dbt_project.yml /opt/dbt/dbt_project.yml
COPY models /opt/dbt

COPY profiles.yml /root/.dbt/profiles.yml

RUN pip install dbt-snowflake==1.8.4
