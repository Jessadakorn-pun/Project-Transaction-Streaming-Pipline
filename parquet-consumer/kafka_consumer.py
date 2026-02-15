from kafka import KafkaConsumer
import json

def create_consumer(bootstrap, group, topics):
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers = bootstrap,
        group_id = group,
        enable_auto_commit = False,
        value_deserializer = lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset = "earliest",
        max_poll_records=500
    )
    return consumer