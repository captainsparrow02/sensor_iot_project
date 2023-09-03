# Sensor IoT Project
This project showcases a comprehensive solution for collecting, storing, and processing data from Internet of Things (IoT) sensors. It demonstrates the seamless integration of sensor data collection, database management, and API-based data retrieval.

## Instructions to run this application.
Clone this repository using the command below.
```sh
git clone https://github.com/captainsparrow02/sensor_iot_project.git
```
This is a containerized application and requires docker for its execution. Make sure that you have docker installed on your machine or [Install Docker Desktop](https://www.docker.com/products/docker-desktop/). 

Once you have Docker installed, navigate to the project folder
```sh
cd sensor_iot_project
```
... and run the command below.
```sh
docker-compose up --build -d
```
Setting up the images and starting up the services may take some time once you see the following message in your terminal, that indicates that the services are up and running.
```sh
.....
Creating mongodb ... done
Creating mqtt    ... done
Creating redis   ... done
Creating subscriber ... done
Creating fastapi    ... done
Creating publisher  ... done
```
You can view the sensor data using the following API endpoints.
* For fetching the latest 10 sensor readings using a specific sensor ID - http://0.0.0.0:8080/sensor/{id} *`# Replace id with sensor ID`*
* For fetching all sensors data for a given date range - http://0.0.0.0:8080/date?start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD} *`# Replace YYYY-MM-DD with date for both start and end date.`*

To view the logs for the `sensor-publish`, `sensor-subscribe` and `backend-api` services, use the following commands.

... for `sensor-publish` logs
```sh
tail -f logs/publish.log 
```
... for `sensor-subscribe` logs
```sh
tail -f logs/subscribe.log 
```
... for `backend_api` logs
```sh
tail -f logs/backend_api.log 
```
*Note: In the event of encountering port errors, it is likely that the default ports assigned to this application are currently in use by other processes or services on your machine. To resolve this issue, you may choose to terminate the conflicting applications or services, or alternatively, modify the port assignments for this application in both the `docker-compose.yml` file and the `project.conf` file located within the `config` repository.*

To stop the container, run the below command
```sh
docker-compose down
```
## Docker Services Insights
## mqtt
* This service is based on the Eclipse Moquitto Image and sets up a persistent Mosquitto broker with configurable settings and data storage, which can be accessed via standard MQTT and WebSocket interfaces on ports 1883 and 9001 respectively.
* It mounts to 3 volumes - 
	1.    `./config`  to  `/mosquitto/config`  allowing the host machine to access the mosquitto configuration files.
	2.  `./data`  to  `/mosquitto/data`  allowing the host machine to persist data between container restarts.
	3. `./logs`  to  `/mosquitto/log`  allowing the host machine to view log messages generated by the container.
* The container is configured to always restart unless explicitly stopped.

## mongodb
* This service is based on the MongoDB Image and sets up a MongoDB database that can be accessed from outside the container through port 27017 and allows data persistence across container restarts.
* The database is being used to store incoming MQTT messages received within the `sensor-subscribe` container.
* It mounts to a single volume at  `./db`  on the host machine to  `/data/db`  inside the container, allowing data stored in the container to persist across restarts and making it accessible from outside the container.

## redis
* This service is based on the Redis image and sets up a Redis instance that can be accessed from outside the container at port 6379 and allows other services to use it as a cache store.
* The Redis database is being used as a cache within the `backend-api` container for API calls.

## sensor-subscribe
* This service is configured to build a container for a sensor subscription service for incoming MQTT messages based on the contents of the `./sensor-subscribe` directory.
* This service mounts to 3 volumes - 
	1.    `./sensor-subscribe` is mounted to `/sensor-subscribe` inside the container, allowing the container to access the code and dependencies defined in the current directory.
	2.    `./config` is mounted to `/sensor-subscribe/config` inside the container, allowing the container to read configuration files.
	3.    `./logs` is mounted to `/sensor-subscribe/subscribe_logs` inside the container, allowing the container to write log files.
* The `depends_on` section specifies that the `sensor-subscribe` service depends on both the `mqtt` and `mongodb` services. This means that the `sensor-subscribe` service will not start until both the `mqtt` and `mongodb` services are up and running.

## sensor-publisher
* This service is configured to build a container for a sensor publishing service to publish incoming sensor payloads on MQTT topics. It is based on the contents of the `./sensor-publish` directory.
* This service mounts to 3 volumes - 
	1.    `./sensor-publish` is mounted to `/sensor-publish` inside the container, allowing the container to access the code and dependencies defined in the current directory.
	2.    `./config` is mounted to `/sensor-publish/config` inside the container, allowing the container to read configuration files.
	3.    `./logs` is mounted to `/sensor-publish/publish_logs` inside the container, allowing the container to write log files.
* The `depends_on` section specifies that the `sensor-publish` service depends on both the `mqtt` and `sensor-subscribe` services. This means that the `sensor-publish` service will not start until both the `mqtt` and `sensor-subscribe` services are up and running.

## backend_api
* As the name suggests, the `backend_api` service builds a container to interact with the databases using the FastAPI application running inside it. It builds itself based on the contents of `./backend_api` directory with the container name as `fastapi`.
* The service exposes port 8080 and maps it to port 80 inside the container, allowing external requests to reach the FastAPI application running inside the container.
* This service mounts to 3 volumes - 
	1.    `./backend_api` is mounted to `/backend_api` inside the container, allowing the container to access the code and dependencies defined in the current directory.
	2.    `./config` is mounted to `/backend_api/config` inside the container, allowing the container to read configuration files.
	3.    `./logs` is mounted to `/backend_api/backend_api_logs` inside the container, allowing the container to write log files.
* The service depends on several other services defined in the Docker Compose file: `mongodb`, `redis`, and `sensor-subscribe`. This means that the `backend_api` service will not start until these dependent services are up and running.

## Design choices

* To obviate the necessity of embedding sensitive information, such as hostnames, ports, and database names, within Python scripts, a centralized configuration file, designated as `project.conf`, has been implemented inside the `config/` repo. This approach enables modifications to be made independently of the script codebase, ensuring greater flexibility and maintainability.

* To facilitate troubleshooting and monitoring, logging capabilities have been integrated into each Python script utilizing the `logging` module. The resulting log files are conveniently stored in a dedicated `logs/` repository, providing a centralized location for analysis and review.

* To simulate real-world IoT sensors, I have developed two Python scripts: `sensor_reading.py` and `sensor_publisher.py`. The `sensor_reading.py` script generates a payload consisting of a randomly generated float value between 0 and 100, representing a simulated sensor reading, along with an ISO8601 timestamp. The `sensor_publisher.py` script serves as a template for sending the payload to temperature and humidity topics via established MQTT connections, thereby mimicking the publication of sensor data.

## Technical Assumptions

* Since there was no mention of the number of sensors generating data, I have assumed 5 sensors for this project.

* The Redis implementation is designed to store the most recently updated ten sensor readings, For the API endpoint to retrieve the latest ten sensor readings, I've implemented caching of the most recent ten readings for each sensor ID. The cache lasts just 10 seconds to minimize time differences, given the sensors publish data every second.

* For the API endpoint fetching sensors data within a date range, I've assumed the range to be in calendar days. Query parameters take dates in `YYYY-MM-DD` format, returning data from midnight (00:00:00) on the start date to one minute before midnight (23:59:59) on the end date, following the ISO8601 standard. For instance, `start_date=2023-08-24` and `end_date=2023-08-27` would retrieve data between `2023-08-24T00:00:00` and `2023-08-27T23:59:59`.

## Challenges Faced
1. **Challenge**: The subscriber and publisher containers were initiating prior to the MongoDB container, leading to the subscriber container failing and rebooting due to its reliance on the MongoDB container for storing data.
**Solution**: Implemented the `depends-on` configuration to guarantee that dependent containers launch only after the containers they rely upon have been successfully initialized.
	
2. **Challenge**: Given the presence of five autonomous sensors that must concurrently publish data, I faced a dilemma regarding code duplication in the implementation process. Furthermore, executing all five Python sensor scripts simultaneously within the `Dockerfile` presented an additional challenge.\
**Solution**: To address these issues, I opted for creating a template sensor file that could be utilized by all five sensor Python scripts to facilitate data publication while minimizing code repetition. Additionally, I employed a shell script to execute all five sensor Python scripts simultaneously, which was subsequently incorporated into the `Dockerfile`.
