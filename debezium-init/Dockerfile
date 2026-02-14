FROM python:3.11-slim

WORKDIR /app

COPY common /app/common

COPY debezium-init /app/debezium-init

WORKDIR /app/debezium-init

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "debezium_create_connector.py"]