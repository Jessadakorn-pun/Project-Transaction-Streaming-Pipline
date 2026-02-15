import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
KAFKA_GROUP = os.getenv("KAFKA_GROUP", "parquet-sink")

TOPICS = [
    "banking_server.public.customers",
    "banking_server.public.accounts",
    "banking_server.public.transactions"
]

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")