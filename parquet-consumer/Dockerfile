FROM python:3.11-slim

WORKDIR /app

COPY common /app/common
COPY parquet-consumer /app/parquet-consumer

WORKDIR /app/parquet-consumer

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "consumer_main.py"]