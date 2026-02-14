import os
import sys
import json
import requests

# defind connection config
DEBEZIUM_URL = os.getenv("DEBEZIUM_URL", "http://debezium:8083")
CONNECTOR_NAME = os.getenv("CONNECTOR_NAME", "postgres-connector")

connector_config = {
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
}

headers = {"Content-Type": "application/json"}

# checking connection if exitsts
def connector_exists() -> bool:
    url = f"{DEBEZIUM_URL}/connectors/{CONNECTOR_NAME}"
    response = requests.get(url)
    
    return response.status_code == 200

# create debezium connector
def create_connector() -> None:
    url = f"{DEBEZIUM_URL}/connectors"
    response = requests.post(url, headers=headers, data=json.dumps(connector_config))
    
    if response.status_code == 201:
        print("-- Connector created successfully --")
        return
    
    if response.status_code == 409:
        print("-- Connector already exists --")
        return

    print(f"-- Failed to create connector with code: {response.status_code} \n -- error: {response.text} \n")
    sys.exit(1)
    
def main():
    
    print("\n========= Debezium Init =========\n")
    
    try:
        if connector_exists():
            print("-- Connector already exists -> skip creation")
        else:
            print("-- Creating connector ...")
            create_connector()
    except requests.exceptions.ConnectionError:
        print("-- Cannot connect to Debezium Connect")
        print(f"URL: {DEBEZIUM_URL}")
        sys.exit(1)
    
if __name__ == "__main__":    
    main()
    