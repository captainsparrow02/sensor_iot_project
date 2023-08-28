import paho.mqtt.client as mqtt
import json
import sensor
import sys
import time

client = None

def on_log(client, userdata, level, buf):
    print("log: ", buf)

# Publishing data
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print(f"{client}: Connected OK")
	else:
		print("Bad connection")
		sys.exit(1)

def publish_data(mqttBroker, mqtt_client, topic, qos, port):
	global client

	client = mqtt_client
	# client.on_log = on_log
	client.on_connect = on_connect
	client.on_log=on_log

	# Connecting client to mqttBroker
	try:
		client.connect(mqttBroker, port)
	except:
		print("No Connection")
		sys.exit(1)


	client.loop_start()
	c = 0
	try:
		while True:
			payload = json.dumps(sensor.get_sensor_payload())
			client.publish(topic, payload, qos)
			c+=1
			print(c)
			time.sleep(2)
	except KeyboardInterrupt:
		print("Closing")
		client.disconnect()
		client.loop_stop()
