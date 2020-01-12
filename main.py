from os import getenv
from time import sleep

from influx_measurement import InfluxMeasurement
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from lib import get_active_sensor_information, get_temp_from_sensor


def setup_db_for_use(host,
                     port,
                     db_name='firefly',
                     retention_duration='1h',
                     retention_policy_name="default_firefly_retention"):
    """
    Sets up an instance of InfluxDB to store data to.

    :param host: the ip which can be used to access the db
    :param port: the port by which the db can be accessed
    :param db_name: name of the databse to use inside InfluxDB
    :param retention_duration: specifies how long to retain the stored information
    :param retention_policy_name: name of the retention policy that is to be created
    :return: an active InfluxDB client
    """
    client = InfluxDBClient(host, port)

    if {"name": db_name} not in client.get_list_database():
        client.create_database(db_name)

    client.switch_database(db_name)
    client.create_retention_policy(retention_policy_name,
                                   retention_duration,
                                   1,
                                   default=True)
    return client


def generate_a_measurement_point(item_name,
                                 sensor_name=None,
                                 sensor_id=None,
                                 sensor_output_file_dir=None,
                                 output_filename="w1_slave"):
    """
    Generates an InfluxDB style measurement point based on the data provided.

    :param item_name: The name of the item the measurement belongs to. i.e. Water Tank, radiator
    :param sensor_id: The unique identifier of the sensor, under which the temp reading output can be found
    :param sensor_name: Name of the sensor
    :param sensor_output_file_dir: directory location of the sensor's output file, with trailing '/'
    :param output_filename: name of the sensor's output file
    :return: An InfluxDB style measurement point
    """
    temp = get_temp_from_sensor(sensor_id=sensor_id,
                                output_file_dir=sensor_output_file_dir,
                                output_filename=output_filename)
    point = InfluxMeasurement(measurement_val=item_name,
                              tag_val=sensor_name,
                              field_val=temp).measurement_point
    return point


def write_data_to_db(client, points_information):
    """
    Writes measurement points to the specified Database.

    :param client: An active instance of InfluxDB
    :param points_information: All measurement points that are to be written; List
    """
    print(points_information)
    try:
        client.write_points(points_information)
    except InfluxDBClientError:
        raise InfluxDBClientError(
            f"error for data entry :: {points_information}")


def main(client, temp_sensors):
    """
    For all specified sensors, genereate measurement points, and then write to DB

    :param client: An active instance of InfluxDB
    :param temp_sensors: All the sensors that should be read; List
    """
    for sensor in temp_sensors:
        point = generate_a_measurement_point(sensor.item, sensor.name,
                                             sensor.id)
        write_data_to_db(client, [point])


if __name__ == "__main__":
    SENSORS_INFO_FILE_NAME = "sensors_info"
    HOST, PORT = [getenv("DBHOST", "localhost"), getenv("DBPORT", "8086")]
    CLIENT = setup_db_for_use(HOST, PORT)
    TEMP_SENSORS = get_active_sensor_information(SENSORS_INFO_FILE_NAME)
    while True:
        main(CLIENT, TEMP_SENSORS)
        sleep(1)
