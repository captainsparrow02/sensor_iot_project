import paho.mqtt.client as mqtt
import multiprocessing
from sensor_publish_template import publish_data

# Using a mqtt broker server.
mqttBroker = "mqtt"

# Creating client and giving it a name.
client_temp = mqtt.Client("Temperature")
client_humid = mqtt.Client("Humidity")
# client.username_pw_set("user1", "1234")
port = 1883
qos = 1
topic_temp = "sensor/reading/temperature"
topic_humid = "sensor/reading/humidity"
# payload = json.dumps(sensor.get_sensor_payload())

temperature = multiprocessing.Process(target = publish_data, args = [
		mqttBroker,
        client_temp,
        topic_temp,
        qos,
        port
        ])

humidity = multiprocessing.Process(target = publish_data, args = [
		mqttBroker,
        client_humid,
        topic_humid,
        qos,
        port
        ])

temperature.start()
humidity.start()
temperature.join()
humidity.join()