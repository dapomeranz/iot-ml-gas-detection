import paho.mqtt.client as paho
import os
import pickle
import json
import numpy as np
from paho import mqtt
from dotenv import load_dotenv

load_dotenv()

model = pickle.load(open("trained_model", "rb"))


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


current_data = []


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global current_data
    data = json.loads(str(msg.payload.decode("utf-8")))
    if "r1" not in data:
        print("data does not look correct")
        return

    cur = []
    cur.append(data["r1"])
    cur.append(data["r2"])
    cur.append(data["r3"])
    cur.append(data["r4"])
    cur.append(data["r5"])
    cur.append(data["r6"])
    cur.append(data["r7"])
    cur.append(data["r8"])
    cur.append(data["temp"])
    cur.append(data["humidity"])
    current_data.append(cur)
    if len(current_data) == 480:
        current_data = np.array(current_data)
        current_data = current_data[np.newaxis, ...]
        print("Model is predicting: ", model.predict(current_data)[0])
        client.publish(
            "mox_sensors/predicted_state",
            payload=json.dumps({"data": model.predict(current_data)[0]}),
            qos=0,
        )
        current_data = []


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))
client.on_subscribe = on_subscribe
client.on_message = on_message

client.subscribe("mox_sensors/#", qos=1)

client.loop_forever()
