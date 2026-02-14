FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY debezium_create_connector.py .

CMD ["python", "debezium_create_connector.py"]