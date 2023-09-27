from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, KafkaError

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'

# Check if the topic exists and create it if it doesn't
def create_topic_if_not_exists(admin_client, topic_name):
    topic_metadata = admin_client.list_topics()
    if topic_name in topic_metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Created topic '{topic_name}'.")

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}

admin_config = {'bootstrap.servers': bootstrap_servers}

admin_client = AdminClient(admin_config)

# Name of the topic to produce to
topic_name = "location-data"

# Create the topic if it doesn't exist
create_topic_if_not_exists(admin_client, topic_name)

# Create a Kafka producer
producer = Producer(producer_config)

try:
    # Produce a message to the topic
    message_value = "This is a sample message."
    producer.produce(topic=topic_name, value=message_value)

    # Wait for any outstanding messages to be delivered and delivery reports to be received
    producer.flush()

    print(f"Produced message to '{topic_name}': {message_value}")

except Exception as e:
    print(f"Error producing message: {str(e)}")

finally:
    producer.flush()  # Ensure any remaining messages are delivered
