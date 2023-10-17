import time
import paho.mqtt.client as paho
import os
from paho import mqtt
from data_fetcher import generator_next_data_row
from dotenv import load_dotenv

load_dotenv()


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe("mox_sensors/#", qos=1)

client.loop_start()

while True:
    client.publish(
        "mox_sensors/live2",
        payload=next(generator_next_data_row()),
        qos=0,
    )
    time.sleep(0.05)
