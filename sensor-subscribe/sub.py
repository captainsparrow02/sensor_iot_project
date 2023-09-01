import paho.mqtt.client as mqtt
from configparser import ConfigParser
import sys
from pymongo import MongoClient
import json
import logging as log

# Initializing Logging
log.basicConfig(filename='subscribe_logs/subscribe.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

# Initializing Configuration Parser to read config file
config = ConfigParser()
config.read("config/project.conf")

# Setting up MongoDB
mongo_client = MongoClient(config["MONGODB"]["hostname"])
db = mongo_client[config["MONGODB"]["db"]]
collections_temp = db[config["MONGODB"]["temperature_collection"]]
collections_humid = db[config["MONGODB"]["humidity_collection"]]

# Setting up MQTT
client = mqtt.Client("Subscriber")
mqttBroker = config["MQTT"]["broker"]
port = int(config["MQTT"]["port"])
qos = int(config["MQTT"]["subscribe_qos"])
topic_temp = config["MQTT"]["temperature_topic"]
topic_humid = config["MQTT"]["humidity_topic"]

def on_log(client, userdata, level, buf):
    '''Callback function to record logs.'''
    log.info(buf)

def on_connect(client, userdata, flags, response_code):
    '''Callback function triggered at connection to broker.'''
    if response_code == 0:
        log.info(f"{client._client_id}: Connected with status RP {response_code}")

        # Subscribing to topics.
        client.subscribe(topic_humid, qos)
        client.subscribe(topic_temp, qos)

        # Setting callback functions.
        client.message_callback_add(topic_humid, on_message_for_temperature)
        client.message_callback_add(topic_temp, on_message_for_humidity)
    else:
        log.warning(f"{client._client_id}: Bad Connection.")

def on_message_for_temperature(client, userdata, message):
    '''Callback function to recieve messages on temperature topic.'''

    log.info(f"{client._client_id}: Recieved Message on temp- "+str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))

    # Storing recieved payload to MongoDB.
    try:
        collections_temp.insert_one(payload)
        log.info("Data inserted in DB.")
    except Exception as e:
        log.warning("Data could not be inserted.")
        log.warning(str(e))

def on_message_for_humidity(client, userdata, message):
    '''Callback function to recieve messages on humidity topic.'''

    log.info(f"{client._client_id}: Recieved Message on humid- "+str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))

    # Storing recieved payload to MongoDB.
    try:
        collections_humid.insert_one(payload)
        log.info("Data inserted in DB.")
    except Exception as e:
        log.warning("Data could not be inserted.")
        log.warning(str(e))
    
client.on_connect = on_connect
client.on_log=on_log

# Connecting to broker.
try:
	client.connect(mqttBroker, port)
except:
	log.warning(f"{client._client_id}: Could not connect.")
	sys.exit(1)

# Looping infinitely to recieve messages on topics.
client.loop_forever()
