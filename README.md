# Sensor IoT Project
This project showcases a comprehensive solution for collecting, storing, and processing data from Internet of Things (IoT) sensors. It demonstrates the seamless integration of sensor data collection, database management, and API-based data retrieval.

## Instructions to run this application.
Clone this repository using the command below.
```sh
git clone https://github.com/captainsparrow02/sensor_iot_project.git
```
This is a containerized application and requires docker for it to run. Make sure that you have docker installed on your machine or [Install Docker Desktop](https://www.docker.com/products/docker-desktop/). 

Once you have Docker installed, navigate to the project folder
```sh
cd sensor_iot_project
```
... and run the command below.
```sh
docker-compose up --build -d
```
Setting up the images and starting up the services may take some time. Once you see the following message in your terminal, that indicates that the services are up and running.
```sh
.....
Creating mongodb ... done
Creating mqtt    ... done
Creating redis   ... done
Creating subscriber ... done
Creating fastapi    ... done
Creating publisher  ... done
```
You can view the sensor data using the following API-endpoints.
* For fetching latest 10 sensor readings using a specific sensor ID - http://0.0.0.0:8080/sensor/{id}
* For fetching all sensors data for a given date range - http://0.0.0.0:8080/date?start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}

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

## Design choices

* To obviate the necessity of embedding sensitive information, such as hostnames, ports, and database names, within Python scripts, a centralized configuration file, designated as `project.conf`, has been implemented inside the `config/` repo. This approach enables modifications to be made independently of the script codebase, ensuring greater flexibility and maintainability.

* To facilitate troubleshooting and monitoring, logging capabilities have been integrated into each Python script utilizing the `logging` module. The resulting log files are conveniently stored in a dedicated `logs/` repository, providing a centralized location for analysis and review.

* To simulate real-world IoT sensors, I have developed two Python scripts: `sensor_reading.py` and `sensor_publisher.py`. The `sensor_reading.py` script generates a payload consisting of a randomly generated float value between 0 and 100, representing a simulated sensor reading, along with an ISO8601 timestamp. The `sensor_publisher.py` script serves as a template for sending the payload to temperature and humidity topics via established MQTT connections, thereby mimicking the publication of sensor data.

## Technical Assumptions

* Since there was no mention on the number of sensors generating data, I have assumed 5 sensors for this project.

* The Redis implementation is designed to store the most recently updated ten sensor readings, For the API endpoint to retrieve the latest ten sensor readings, I've implemented caching of the most recent ten readings for each sensor ID. The cache lasts just 10 seconds to minimize time differences, given the sensors publish data every second.