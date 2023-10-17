## IoT Data Science Project

This repo contains three parts:

1. A simulator to stream continuous data from a dataset over an MQTT broker as if it were real data coming from IoT sensors. With default run speed (20 rows per second) there is around 13 hours of data.
2. A Jupyter Notebook where an ML model was trained to predict what classification the sensors are currently emitting. The model was trained on the data from the simulator.
3. A python script that subscribes to the broker and utilizes the latest 10,000 points to run the model.


Data can be downloaded from this link and placed in a folder called `data` in this dir.

Need to add MQTT broker credentials to the .env file in the following format:

  ```
  MQTT_HOST=xxx
  MQTT_PORT=xxx
  MQTT_USERNAME=xxx
  MQTT_PASSWORD=xxx
  ```

## Running the simulator

1. Create a virtual environment and install the requirements from the requirements.txt file.
2. Run `mqtt_publish.py`


