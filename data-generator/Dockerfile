FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# copy source
COPY common /app/common
COPY data-generator /app/data-generator


WORKDIR /app/data-generator

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "data_generator_main.py"]