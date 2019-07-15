"""
A library of helper methods used by main.py
"""

import re
from collections import namedtuple

SENSOR = namedtuple("SENSOR", "item name id")


def _read_data_from_sensor_file(sensor_name):
    """Reads all data from the sensor's log file."""

    f_location = "/w1_bus_master1/" + sensor_name + "/"
    f = open(f_location + "w1_slave", "r")
    f_data = f.readlines()
    f.close()
    return f_data


def get_temp_from_sensor(sensor_name):
    """Gets the tempearture data from sensor"""
    lines = _read_data_from_sensor_file(sensor_name)
    temp_data = re.search('t=[0-9]*', lines[1])[0]
    celcius = float(temp_data[2:]) / 1000
    return celcius
