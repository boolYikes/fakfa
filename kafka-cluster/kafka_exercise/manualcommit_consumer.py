import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

import json

from kafka import TopicPartition, OffsetAndMetadata
from kafka.consumer import KafkaConsumer


def key_deserializer(key):
    return key.decode('utf-8')


def value_deserializer(value):
    return json.loads(value.decode('utf-8'))


def main():
    topic_name = "fake_people"
    bootstrap_servers = ["localhost:9092"]
    consumer_group_id = "manual_fake_people_group"

    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id=consumer_group_id,
        key_deserializer=key_deserializer,
        value_deserializer=value_deserializer,
        auto_offset_reset='earliest',
        enable_auto_commit=False)

    consumer.subscribe([topic_name])
    for record in consumer:
        print(f"""
            Consumed person {record.value} with key '{record.key}'
            from partition {record.partition} at offset {record.offset}
        """)

        topic_partition = TopicPartition(record.topic, record.partition)
        offset = OffsetAndMetadata(record.offset + 1, record.timestamp)
        consumer.commit({
            topic_partition: offset
        })

if __name__ == '__main__':
    main()