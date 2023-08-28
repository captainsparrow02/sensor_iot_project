import paho.mqtt.client as mqtt
import sys
import pymongo
import json
# import redis

# MongoDB
mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = mongo_client['sensors']
collections_temp = db['temp']
collections_humid = db['humid']

# MQTT 
client = mqtt.Client("Subscriber")
mqttBroker = "mqtt"
port = 1883
topic_humidity = "sensor/reading/humidity"
topic_temperature = "sensor/reading/temperature"
# client.username_pw_set("user1","1234")
qos = 0

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_connect(client, userdata, flags, response_code):
	# Checking for established connection.
    if response_code == 0:
        conFlag = True
        print("Connected with status: {0}".format(response_code))	
        client.subscribe(topic_humidity, qos)
        client.subscribe(topic_temperature, qos)
        client.message_callback_add(topic_humidity, on_message_for_temperature)
        client.message_callback_add(topic_temperature, on_message_for_humidity)
    else:
        print("Bad Connection", response_code)

def on_message_for_temperature(client, userdata, message):
    print("Recieved Message: ", str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))

    print("temp", payload)
    try:
        collections_temp.insert_one(payload)
    except Exception as e:
        print("Data could not be inserted.")
        print(e)

    # redis_client.lpush("sensor_readings", json.dumps(payload))
    # redis_client.ltrim("sensor_readings", 0, 9)
    # collections.insert_one(payload)

def on_message_for_humidity(client, userdata, message):
    print("Recieved Message: ", str(message.payload.decode('utf-8')))
    payload = json.loads(message.payload.decode('utf-8'))
    print("Humid", payload)
    try:
        collections_humid.insert_one(payload)
    except:
        print("Data could not be inserted.")

# Attempting Connection
client.on_connect = on_connect
# client.on_message = on_message
# client.on_log=on_log

try:
	client.connect(mqttBroker, port)
except:
	print("No Connection")
	sys.exit(1)
client.loop_forever()
