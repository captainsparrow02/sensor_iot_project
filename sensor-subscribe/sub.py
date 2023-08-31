import paho.mqtt.client as mqtt
from configparser import ConfigParser
import sys
from pymongo import MongoClient
import json
import logging as log

log.basicConfig(filename='subscribe_logs/subscribe.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

config = ConfigParser()
config.read("config/project.conf")

# MongoDB
mongo_client = MongoClient(config["MONGODB"]["hostname"])
db = mongo_client[config["MONGODB"]["db"]]
collections_temp = db[config["MONGODB"]["temperature_collection"]]
collections_humid = db[config["MONGODB"]["humidity_collection"]]

# MQTT 
client = mqtt.Client("Subscriber")
mqttBroker = config["MQTT"]["broker"]
port = int(config["MQTT"]["port"])
qos = int(config["MQTT"]["subscribe_qos"])
topic_temp = config["MQTT"]["temperature_topic"]
topic_humid = config["MQTT"]["humidity_topic"]

def on_log(client, userdata, level, buf):
    log.info(buf)

def on_connect(client, userdata, flags, response_code):
	# Checking for established connection.
    if response_code == 0:
        conFlag = True
        log.info(f"{client._client_id}: Connected with status RP {response_code}")	
        client.subscribe(topic_humid, qos)
        client.subscribe(topic_temp, qos)
        client.message_callback_add(topic_humid, on_message_for_temperature)
        client.message_callback_add(topic_temp, on_message_for_humidity)
    else:
        log.warning(f"{client._client_id}: Bad Connection.")

def on_message_for_temperature(client, userdata, message):
    log.info(f"{client._client_id}: Recieved Message on temp- "+str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))

    try:
        collections_temp.insert_one(payload)
        log.info("Data inserted in DB.")
    except Exception as e:
        log.warning("Data could not be inserted.")
        log.warning(str(e))

def on_message_for_humidity(client, userdata, message):
    log.info(f"{client._client_id}: Recieved Message on humid- "+str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))

    try:
        collections_humid.insert_one(payload)
        log.info("Data inserted in DB.")
    except Exception as e:
        log.warning("Data could not be inserted.")
        log.warning(str(e))
    
client.on_connect = on_connect
client.on_log=on_log

try:
	client.connect(mqttBroker, port)
except:
	log.warning(f"{client._client_id}: Could not connect.")
	sys.exit(1)
client.loop_forever()
