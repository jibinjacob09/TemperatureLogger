"""The measurement point data needs to be in the following JSON format, and the class below will act as a factory to
generate the points which can then be written to InfluxDB.
"""


class InfluxMeasurement:
    """A new measurement point is created using the schema for each class instance"""

    def __init__(self, measurement_val, tag_val, field_val=0):
        """Schema for the db, which should be modified to match the usecase

        :param measurement_val: The name of the item being measured; example "Resorvoir", "tube"
        :param tag_val: name of the sensor
        """
        self._schema = {
            "measurement": measurement_val,
            "tags": {
                "sensor": tag_val
            },
            "fields": {
                "temp": field_val
            }
        }

    @property
    def measurement_point(self):
        """Returns a influxdb measurement point defined by the schema"""
        return self._schema

    @measurement_point.setter
    def measurement_point(self, point_dict):
        """Overwrite the generated influxdb measurement point"""
        self._schema = point_dict
