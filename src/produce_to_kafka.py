import requests
import time
import json
import logging
from confluent_kafka import Producer


# Makes an api call to fetch weather data from the API endpoint
def get_weather() -> dict:
    # Fetch weather data from the API
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 1.2897,
            "longitude": 103.8501,
            "current_weather": "true",
        },
    )
    return response.json()


def main():
    # Configure logging level
    logging.basicConfig(level=logging.DEBUG)

    # Kafka producer configuration, specifies the broker address
    producer_config = {"bootstrap.servers": "localhost:9092"}

    # Create a Kafka producer by passing in the producer config
    producer = Producer(producer_config)

    """
    1) Wrap the logic into a try except finally block using, allows you to interrupt 
    2) while loop to ensure that whenever data is available, kafka reads from it
    """
    try:
        while True:
            # Get the weather data
            weather = get_weather()
            logging.debug("Got weather: %s", weather)

            # Produce the weather data to Kafka
            producer.produce(
                topic="weather_data_demo",
                key="Singapore",
                # dumps converts the json into a string type, encoded into bytes as kafka messages are sent in bytes
                value=json.dumps(weather).encode("utf-8"),
            )
            logging.info("Produced weather data. Interval of 5 seconds...")

            # Ensure all messages are sent before the script pauses
            producer.flush()

            # Simulate intervals of 5 seconds
            time.sleep(5)

    except KeyboardInterrupt:
        logging.info("Stopping the producer.")
    finally:
        # Flush
        producer.flush()


if __name__ == "__main__":
    main()
