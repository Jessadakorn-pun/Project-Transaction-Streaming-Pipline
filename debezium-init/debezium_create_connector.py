import os
import sys
import json
import requests
import logging
import time
from config import (DEBEZIUM_URL, CONNECTOR_NAME, HEADERS, CONNECTOR_CONFIG, RETRY_MAX, RETRY_INTERVAL)
from common.logging import setup_logging

# setting logger
setup_logging("debezium-init")
logger = logging.getLogger(__name__)
    
# checking debezium service
def wait_for_debezium_ready() -> None:
    logger.info("Waiting for Debezium Connect to be ready ...")
    url = f"{DEBEZIUM_URL}/connectors"
    for attempt in range(1, RETRY_MAX + 1):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info("Debezium Connect is ready")
                return
        except requests.exceptions.RequestException:
            pass
        
        logger.warning(f"Debezium not ready (attempt {attempt} / {RETRY_MAX})")
        time.sleep(RETRY_INTERVAL)
    logger.error("Debezium Connect not ready after retries")
    
# checking connection if exitsts
def connector_exists() -> bool:
    url = f"{DEBEZIUM_URL}/connectors/{CONNECTOR_NAME}"
    response = requests.get(url)
    
    return response.status_code == 200

# create debezium connector
def create_connector(connector: dict) -> None:
    url = f"{DEBEZIUM_URL}/connectors"
    response = requests.post(url, headers=HEADERS, data=json.dumps(connector))
    
    if response.status_code == 201:
        logger.info(f"Connector created successfully: {connector['name']}")
        return
    
    elif response.status_code == 409:
        print(f"Connector already exists: {connector['name']}")
        return

    else:
        logger.error(
            f"Failed to create connector: {connector['name']} |"
            f"status={response.status_code} | body={response.text}"
        )
        sys.exit(1)
        
# create connection 
def create_connection(connector: dict) -> None:
    if connector_exists():
        logger.info(f"Skip existing connector: {connector['name']}")
    else:
        logger.info(f"Creating connector: {connector['name']}")
        create_connector(connector)
    
def main():

    logger.info("Debezium Init Start")
    
    wait_for_debezium_ready()
    
    for connector in CONNECTOR_CONFIG:
        create_connection(connector)
    
    logger.info("Debezium Init Complete")

    
if __name__ == "__main__":    
    main()
    