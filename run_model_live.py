import paho.mqtt.client as paho
import os
from sktime.base import load
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()

model = load("trained_sktime_model")

lookup = np.loadtxt("data/HT_Sensor_metadata.dat", skiprows=1, dtype=str)


def get_class(data):
    if data["time"] < 0:
        return "background"
    length_of_time = lookup[lookup[:, 0] == str(data["id"])][0][4]
    if data["time"] > float(length_of_time):
        return "background"
    ## lookup data["id"] in the first column of the lookup and return the 3rd column
    return lookup[lookup[:, 0] == str(data["id"])][0][2]


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
    ## Once the data collection gets to 120 rows, we can start predicting
    ## Then remove the first 60 rows and the data will gather 60 more points for the next prediction
    if len(current_data) == 120:
        np_array = np.array(current_data)
        np_array = np_array[np.newaxis, ...]
        prediction = model.predict(np_array)[0]
        print("Model is predicting: ", prediction)
        print("Actual current state: ", get_class(data))
        client.publish(
            f"{os.getenv('MQTT_TOPIC_PREFIX')}/predicted_state",
            payload=json.dumps({"data": prediction}),
        )
        del current_data[0:60]


client = paho.Client()
client.on_connect = on_connect

## NOT NEEDED FOR PUBLIC BROKER
# from paho import mqtt
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))

client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))
client.on_subscribe = on_subscribe
client.on_message = on_message

client.subscribe(f"{os.getenv('MQTT_TOPIC_PREFIX')}/data")

client.loop_forever()
