"""
A library of helper methods used by main.py
"""

import re
from collections import namedtuple


def _read_data_from_file(full_file_path):
    """Reads all data from the sensor's log file, originally designed for sensors in rasp Pi

    :param full_file_path: the path to the sensor output file
    """

    _file = open(full_file_path, "r")
    file_data = _file.read()
    _file.close()
    return file_data


def get_temp_from_sensor(sensor_id=None, output_file_dir=None, output_filename="w1_slave"):
    """Gets the tempearture data from sensor, designed for DS18B20.

    :param sensor_id: unique id of the sensor, used to locate its output file if output_file_dir is not provided
    :param output_file_dir: directory location of the sensor's output file, with trailing '/'
    :param output_filename: name of the sensor's output file
    """

    file_location = output_file_dir if output_file_dir is not None else f"/w1_bus_master1/{sensor_id}/"
    file_data = _read_data_from_file(full_file_path=f"{file_location}{output_filename}")

    try:
        temp_data = re.search('t=[0-9]+', file_data)[0]
        celcius = float(temp_data[2:]) / 1000
    except TypeError:
        celcius = -1  # temp data could not be read from the output file

    return celcius


def get_active_sensor_information(sensor_file_path):
    """Parse the info from sensors_file, and then create a data object for each sensor.

    :param sensor_file_path: file path to sensors_info file
    :return a named tuple with item, id, name as fields
    """
    sensor = namedtuple("sensor", "item id name")
    lst_sensors = []

    f_lines = _read_data_from_file(sensor_file_path).split("\n")
    if len(f_lines) <= 1:
        raise ValueError("A valid sensor_info file is missing. Please populate one by following the example")

    for data_line in f_lines[1:]:
        try:
            lst_sensors.append(sensor._make(data_line.split(",")))
        except TypeError:
            raise ValueError("A valid sensor_info file is missing. Please populate one by following the example")

    return lst_sensors
