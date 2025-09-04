#!/usr/bin/env python3

import numpy as np
import pandas as pd
from data.PFCS.scripts.gt_plot import read_data
from pathlib import Path


DATAPATH_ROOT = Path("./data/PFCS/table task")

TASK_GROUND_TRUTH = [
    {
        "filename": "fetch_recorded_demo_1730997119",
        "idx": {
            "plate": {"ini": 0, "end": 1125},
            "napkin": {"ini": 1125, "end": 2591},
            "cup": {"ini": 2591, "end": 3986},
            "fork": {"ini": 3986, "end": 5666},
            "spoon": {"ini": 5666, "end": 7338},
        },
    },
    {
        "filename": "fetch_recorded_demo_1730997530",
        "idx": {
            "plate": {"ini": 0, "end": 1812},
            "napkin": {"ini": 1812, "end": 3844},
            "cup": {"ini": 3844, "end": 5732},
            "fork": {"ini": 5732, "end": 7090},
            "spoon": {"ini": 7090, "end": 7955},
        },
    },
    {
        "filename": "fetch_recorded_demo_1730997735",
        "idx": {
            "plate": {"ini": 0, "end": 1965},
            "napkin": {"ini": 1965, "end": 4178},
            "cup": {"ini": 4178, "end": 6427},
            "spoon": {"ini": 6427, "end": 7904},
            "fork": {"ini": 7904, "end": 9123},
        },
    },
    {
        "filename": "fetch_recorded_demo_1730997956",
        "idx": {
            "plate": {"ini": 0, "end": 1898},
            "napkin": {"ini": 1898, "end": 4081},
            "cup": {"ini": 4081, "end": 5442},
            "spoon": {"ini": 5442, "end": 6829},
            "fork": {"ini": 6829, "end": 9177},
        },
    },
]


def data2df(filenum, timestamps=True, datapath_root=DATAPATH_ROOT):
    xyz_path = (
        datapath_root
        / "xyz data"
        / "full_tasks"
        / (TASK_GROUND_TRUTH[filenum]["filename"] + ".txt")
    )
    h5_path = (
        datapath_root / "h5 files" / (TASK_GROUND_TRUTH[filenum]["filename"] + ".h5")
    )

    data = np.loadtxt(xyz_path)  # load the file into an array
    joint_data, tf_data, gripper_data = read_data(h5_path)

    if timestamps:
        time_sec = tf_data[0][:, 0]
        time_nanosec = tf_data[0][:, 1]
        timestamps = []
        for t_idx, t_val in enumerate(time_sec):
            timestamp = pd.Timestamp(
                time_sec[t_idx], unit="s", tz="EST"
            ) + pd.to_timedelta(time_nanosec[t_idx], unit="ns")
            timestamps.append(timestamp)
        timestamps = pd.Series(timestamps)

        traj = pd.DataFrame(
            {
                "x": data[:, 0],
                "y": data[:, 1],
                "z": data[:, 2],
                "timestamps": timestamps,
            }
        )
    else:
        traj = pd.DataFrame({"x": data[:, 0], "y": data[:, 1], "z": data[:, 2]})
    return traj


def get_ground_truth(filenum):
    classes = TASK_GROUND_TRUTH[filenum]["idx"]
    class_vect = np.array([])
    for idx, (key, val) in enumerate(classes.items()):
        current_vect = np.ones((val["end"] - val["ini"])) * (idx + 1)
        class_vect = np.concat((class_vect, current_vect))
    return class_vect
