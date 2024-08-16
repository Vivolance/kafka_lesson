from confluent_kafka import Consumer, KafkaException, KafkaError
import json


def main():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "weather_reader",
        "auto.offset.reset": "latest",
    }

    consumer = Consumer(consumer_config)

    try:
        consumer.subscribe(["weather_data_demo"])

        while True:
            msg = consumer.poll(1.0)  # Poll messages from Kafka

            if msg is None:
                print("Waiting...")
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached
                    continue
                else:
                    raise KafkaException(msg.error())
            else:
                key = msg.key().decode("utf-8") if msg.key() else None
                value = json.loads(msg.value().decode("utf-8"))
                offset = msg.offset()

                print(f"{offset} {key} {value}")
                consumer.commit(asynchronous=False)  # Store offsets

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
