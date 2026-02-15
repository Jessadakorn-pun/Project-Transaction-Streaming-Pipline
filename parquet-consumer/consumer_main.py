from kafka_consumer import create_consumer
from parquet_writer import write_parquet_idempotent
from common.logging import setup_logging
from config import *
import boto3
import logging

# setting up log
setup_logging("kafka_consumer")
logger = logging.getLogger(__name__)

# create kafka cosumer
consumer = create_consumer(KAFKA_BOOTSTRAP, KAFKA_GROUP, TOPICS)

# create s3 connection
s3 = boto3.client(
    "s3",
    endpoint_url = MINIO_ENDPOINT,
    aws_access_key_id = os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key = os.getenv('MINIO_SECRET_KEY'),
)

# create buffer
buffer = {topic: [] for topic in TOPICS}

logger.info("Kafka consumer started")

try:
    for message in consumer:
    
        # extract payload from the message
        payload = message.value.get("payload", {})
        record = payload.get("after")
        
        # check if have data
        if not record:
            continue
        
        # append data in to list
        buffer[message.topic].append(record)
        
        # if size of the buffer reach BATCH_SIZE -> write file to s3
        if len(buffer[message.topic]) >= BATCH_SIZE:
            
            # getting table name from topic: banking_server.public.<table_name>
            table = message.topic.split(".")[-1]
            
            # write file to s3
            write_parquet_idempotent(
                buffer[message.topic],
                table,
                message.offset,
                s3,
                MINIO_BUCKET,
            )

            # commit the process
            consumer.commit()

            # clear buffer
            buffer[message.topic].clear()
            
            logger.info(f"Committed {table} offset={message.offset} row={BATCH_SIZE}")
            
except Exception:
    logger.exception("Failed to processing message")

except KeyboardInterrupt:
    logger.warning("Consumer interruped by user")

finally:
    consumer.close()
    logger.info("Kafka consumer closed")