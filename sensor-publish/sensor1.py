from sensor_publisher import start_publish
import logging as log

# Initializing Logging.
log.basicConfig(filename='publish_logs/publish.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

log.info("Starting Sensor 1.")

# Starting Sensor to publish data.
start_publish("Sensor1", 101)