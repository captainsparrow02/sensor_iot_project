# Sensor IoT Project
This project showcases a comprehensive solution for collecting, storing, and processing data from Internet of Things (IoT) sensors. It demonstrates the seamless integration of sensor data collection, database management, and API-based data retrieval.

### Instructions to run this application.
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
*Note: If you face any port error, that means the ports set by default for this application are already in use on your machine. Either close the existing applications/services running on those ports on your machine or you can modify the ports for this application in the `docker-compose.yml` file and the `project.conf` file inside the `config` repository.*