import paho.mqtt.client as mqtt
from sensor_reading import get_sensor_payload
from configparser import ConfigParser
import json
import logging as log
import sys
import time

log.basicConfig(filename='publish_logs/publish.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

config = ConfigParser()
config.read("config/project.conf")
mqttBroker = config["MQTT"]["broker"]
port = int(config["MQTT"]["port"])
qos = int(config["MQTT"]["publish_qos"])
topic_temp = config["MQTT"]["temperature_topic"]
topic_humid = config["MQTT"]["humidity_topic"]
		
def on_log(client, userdata, level, buf):
	log.info(buf)
	
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		log.info(f"{client._client_id}: Connected OK")
	else:
		log.warning(f"{client._client_id}: Bad connection. Exiting..")
		sys.exit(1)
		
def start_publish(client_id, sensor_id):

	id = sensor_id
	client = mqtt.Client(client_id)
	
	client.on_log = on_log
	client.on_connect = on_connect
	
	try:
		client.connect(mqttBroker, port)
	except:
		log.warning(f"{client._client_id}: Could not connect.")
		sys.exit(1)
		
	client.loop_start()
	try:
		while True:
			payload_temp = get_sensor_payload()
			payload_temp.update({"sensor_id": id})
			payload_humid = get_sensor_payload()
			payload_humid.update({"sensor_id": id})
			client.publish(topic_temp, json.dumps(payload_temp), qos)
			client.publish(topic_humid, json.dumps(payload_humid), qos)
			time.sleep(1)
	except KeyboardInterrupt:
		log.info(f"{client._client_id}: Closing")
		client.disconnect()
		client.loop_stop()
