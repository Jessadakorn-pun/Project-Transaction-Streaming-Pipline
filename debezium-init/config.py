import os
from typing import List

# defind connection config
DEBEZIUM_URL = os.getenv("DEBEZIUM_URL", "http://debezium:8083")
CONNECTOR_NAME = os.getenv("CONNECTOR_NAME", "postgres-connector")

HEADERS = {"Content-Type": "application/json"}

RETRY_MAX = int(os.getenv("RETRY_MAX", "30"))
RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL", "5"))

CONNECTOR_CONFIG: List[dict] = [
    {
        "name": "postgres-connector",
        "config": {
            
            # Connection to postgres
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "database.hostname": os.getenv("POSTGRES_HOST"),
            "database.port": os.getenv("POSTGRES_PORT"),
            "database.user": os.getenv("POSTGRES_USER"),
            "database.password": os.getenv("POSTGRES_PASSWORD"),
            "database.dbname": os.getenv("POSTGRES_DB"),
            
            # CDC / Kafka
            "topic.prefix": "banking_server",
            "table.include.list": "public.customers,public.accounts,public.transactions",
            
            # WAL / replication
            "plugin.name": "pgoutput",
            "slot.name": "banking_slot",
            "publication.autocreate.mode": "filtered",
            
            # Kafka behavior
            "tombstones.on.delete": "false",
            "decimal.handling.mode": "double",
        },
    },
]