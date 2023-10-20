import time
import paho.mqtt.client as paho
import os
from data_fetcher import generator_next_data_row
from dotenv import load_dotenv

load_dotenv()


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.on_connect = on_connect

## NOT NEEDED FOR PUBLIC BROKER
# from paho import mqtt
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))

client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe(f"{os.getenv('MQTT_TOPIC_PREFIX')}/data")

client.loop_start()

while True:
    client.publish(
        f"{os.getenv('MQTT_TOPIC_PREFIX')}/data",
        payload=next(generator_next_data_row()),
    )
    time.sleep(1)
