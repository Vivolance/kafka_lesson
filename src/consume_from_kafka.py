from confluent_kafka import Consumer, KafkaException, KafkaError
import json


def main():
    # Specifies the kafka address to port 9092
    # Label a consumer group ID
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "weather_reader",
        "auto.offset.reset": "latest",
    }
    # Create a consumer instance
    consumer = Consumer(consumer_config)

    try:
        # Consumers subscribes to a topic
        consumer.subscribe(["weather_data_demo"])

        while True:
            # Consumes at every 1s
            msg = consumer.poll(1.0)

            if msg is None:
                print("Waiting...")
            elif msg.error():
                # continues when consumed the last item in the partition
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached
                    continue
                else:
                    # stop the consumer if an error is faced
                    raise KafkaException(msg.error())
            else:
                # Decode the message (key value pairs) from bytes into strings
                key = msg.key().decode("utf-8") if msg.key() else None
                value = json.loads(msg.value().decode("utf-8"))
                # Retrieves the offset (bookmark) of the message within the partition
                offset = msg.offset()

                print(f"{offset} {key} {value}")
                # Store offsets synchronously
                consumer.commit(asynchronous=False)
    # Allows for ctrl + c without crashing
    except KeyboardInterrupt:
        pass
    finally:
        # Ensures the consumer closes gracefully, allowing all resources to be released and all commits complete.
        consumer.close()


if __name__ == "__main__":
    main()
