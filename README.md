## How to write an application to Kafka
This kafka application makes real-time API calls to open-meteo weather site and reads the current weather parameters and
produces it to a kafka topic, which can then be consumed

### Step 1: Start Zookeeper on your local
Navigate to where your local kafka folder is at then in the commandline:
```commandline
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Step 2: Initiate your kafka Broker
Navigate to where your local kafka folder is at then in the commandline:
```commandline
bin/kafka-server-start.sh config/server.properties
```

### Step 3: Start running your producer and consumer scripts
You should see weather information being produced to the topic every 3 seconds