from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from time import sleep
from firefly_backend.lib import get_temp_from_sensor, SENSOR
from firefly_backend.db_schema import DBSchema

TEMP_SENSORS = [SENSOR("item_name", "sensor_name", "sensor_id")]


def setup_db_for_use(host="localhost", port=8086, db_name='firefly', retention_duration='1h'):
    client = InfluxDBClient(host, port)
    client.switch_database(db_name)
    client.create_retention_policy('default_firefly_retention', retention_duration, 1, default=True)
    return client


def generate_a_measurement_point(item_name, sensor_name, sensor_id):
    temp = get_temp_from_sensor(sensor_id)
    point = DBSchema(measurement_val=item_name, tag_val=sensor_name, field_val=temp).measurement_point
    return point


def write_data_to_db(client, points_information):
    try:
        client.write_points([points_information])
    except InfluxDBClientError:
        raise InfluxDBClientError(f"error for data entry :: {points_information}")


def main(client, temp_sensors):
    for sensor in temp_sensors:
        point = generate_a_measurement_point(sensor.item, sensor.name, sensor.id)
        write_data_to_db(client, point)


if __name__ == "__main__":
    CLIENT = setup_db_for_use()
    for i in range(60):
        main(CLIENT, TEMP_SENSORS)
        sleep(1)
