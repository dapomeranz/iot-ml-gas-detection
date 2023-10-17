import json
import pandas as pd
import numpy as np
from itertools import cycle

data = np.loadtxt("data/HT_Sensor_dataset.dat", skiprows=1)

dataset = pd.DataFrame(
    {
        "id": data[:, 0],
        "time": data[:, 1],
        "r1": data[:, 2],
        "r2": data[:, 3],
        "r3": data[:, 4],
        "r4": data[:, 5],
        "r5": data[:, 6],
        "r6": data[:, 7],
        "r7": data[:, 8],
        "r8": data[:, 9],
        "temp": data[:, 10],
        "humidity": data[:, 11],
    }
)
dataset["id"] = dataset["id"].astype(int)

# Create an infinite cycle over the DataFrame rows
data_cycle = cycle(dataset.iterrows())


def generator_next_data_row():
    while True:
        _, row = next(data_cycle)
        yield json.dumps(
            {
                "id": row["id"],
                "time": row["time"],
                "r1": row["r1"],
                "r2": row["r2"],
                "r3": row["r3"],
                "r4": row["r4"],
                "r5": row["r5"],
                "r6": row["r6"],
                "r7": row["r7"],
                "r8": row["r8"],
                "temp": row["temp"],
                "humidity": row["humidity"],
            }
        )
