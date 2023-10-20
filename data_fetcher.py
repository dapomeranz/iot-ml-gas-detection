import json
import numpy as np
from itertools import cycle

data = np.loadtxt("data/HT_Sensor_dataset.dat", skiprows=1)

data_cycle = cycle(iter(data))

column_names = [
    "id",
    "time",
    "r1",
    "r2",
    "r3",
    "r4",
    "r5",
    "r6",
    "r7",
    "r8",
    "temp",
    "humidity",
]


def generator_next_data_row():
    while True:
        row = next(data_cycle)
        row_dict = {col_name: value for col_name, value in zip(column_names, row)}
        row_dict["id"] = int(row_dict["id"])
        yield json.dumps(row_dict)
