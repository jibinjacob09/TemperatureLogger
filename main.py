from time import sleep
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from lib import get_temp_from_sensor, SENSOR
from db_schema import InfluxMeasurement

TEMP_SENSORS = [SENSOR("item_name", "sensor_id", "sensor_name")]


def setup_db_for_use(host="localhost", port=8086, db_name='firefly', retention_duration='1h'):
    """
    Sets up an instance of InfluxDB to store data to.

    :param host: the ip which can be used to access the db
    :param port: the port by which the db can be accessed
    :param db_name: name of the databse to use inside InfluxDB
    :param retention_duration: specifies how long to retain the stored information
    :return: an active InfluxDB client
    """
    client = InfluxDBClient(host, port)
    client.switch_database(db_name)
    client.create_retention_policy('default_firefly_retention', retention_duration, 1, default=True)
    return client


def generate_a_measurement_point(item_name, sensor_id, sensor_name=None):
    """
    Generates an InfluxDB style measurement point based on the data provided.

    :param item_name: The name of the item the measurement belongs to. i.e. Water Tank, radiator
    :param sensor_id: The unique identifier of the sensor, under which the temp reading output can be found
    :param sensor_name: Name of the sensor
    :return: An InfluxDB style measurement point
    """
    temp = get_temp_from_sensor(sensor_id)
    point = InfluxMeasurement(measurement_val=item_name, tag_val=sensor_name, field_val=temp).measurement_point
    return point


def write_data_to_db(client, points_information):
    """
    Writes measurement points to the specified Database.

    :param client: An active instance of InfluxDB
    :param points_information: All measurement points that are to be written; List
    """
    try:
        client.write_points([points_information])
    except InfluxDBClientError:
        raise InfluxDBClientError(f"error for data entry :: {points_information}")


def main(client, temp_sensors):
    """
    For all specified sensors, genereate measurement points, and then write to DB

    :param client: An active instance of InfluxDB
    :param temp_sensors: All the sensors that should be read; List
    """
    for sensor in temp_sensors:
        point = generate_a_measurement_point(sensor.item, sensor.name, sensor.id)
        write_data_to_db(client, point)


if __name__ == "__main__":
    CLIENT = setup_db_for_use()
    for i in range(60):
        main(CLIENT, TEMP_SENSORS)
        sleep(1)
