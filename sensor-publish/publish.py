import paho.mqtt.client as mqtt
import json
import sensor
import sys
import time

# MQTT
client = mqtt.Client("Sensor")
mqttBroker = "mqtt"
port = 1883
qos = 1
topic_temp = "sensor/reading/temperature"
topic_humid = "sensor/reading/humidity"

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print(f"{client}: Connected OK")
	else:
		print("Bad connection")
		sys.exit(1)


client.on_connect = on_connect
client.on_log=on_log

try:
	client.connect(mqttBroker, port)
except:
	print("No Connection")
	sys.exit(1)


client.loop_start()
try:
	while True:

		payload_temp = json.dumps(sensor.get_sensor_payload())
		payload_humid = json.dumps(sensor.get_sensor_payload())

		client.publish(topic_temp, payload_temp, qos)
		client.publish(topic_humid, payload_humid, qos)
		
		time.sleep(1)
except KeyboardInterrupt:
	print("Closing")
	client.disconnect()
	client.loop_stop()
