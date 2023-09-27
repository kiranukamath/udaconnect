from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, KafkaError

# Kafka broker configuration
bootstrap_servers = 'kafka.default.svc.cluster.local:9092'

# Check if the topic exists and create it if it doesn't
def create_topic_if_not_exists(admin_client, topic_name):
    topic_metadata = admin_client.list_topics()
    if topic_name in topic_metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Created topic '{topic_name}'.")

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
}

admin_config = {'bootstrap.servers': bootstrap_servers}

admin_client = AdminClient(admin_config)

# Name of the topic to consume from
topic_name = "location-data"

# Create the topic if it doesn't exist
create_topic_if_not_exists(admin_client, topic_name)

# Create a Kafka consumer
consumer = Consumer(consumer_config)

# Subscribe to the topic
consumer.subscribe([topic_name])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Reached end of partition for topic {msg.topic()}")
            else:
                print(f"Error while consuming from topic {msg.topic()}: {msg.error()}")
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
