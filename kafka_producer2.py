from kafka import KafkaProducer

# Replace 'localhost' and '9092' with the actual IP address and port of the Kafka broker.
kafka_broker = 'localhost:9092'

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=kafka_broker)

# Your Kafka topic and message data
topic = 'location-data'
message_data = 'Hello, Kafka!'

# Produce a message to the Kafka topic
try:
    producer.send(topic, value=message_data.encode('utf-8'))
    print(f"Produced message to '{topic}': {message_data}")

except Exception as e:
    print(f"Error producing message: {str(e)}")


# Close the Kafka producer
producer.close()
