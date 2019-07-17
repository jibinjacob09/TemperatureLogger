from influxdb import InfluxDBClient
import main


class TestMain:
    """ Influxdb docker container must be running for these tests """

    test_client = main.setup_db_for_use(db_name="testDB", retention_policy_name="testRetention")
    expected_temp_val = 29.191  # taken from sensor_out_valid.txt

    def test_setup_db_for_use_retruns_right_client(self):
        """Connecting to the DB returns an InfluxDBClient object """

        assert isinstance(self.test_client, InfluxDBClient) is True

    def test_setup_db_for_use_retention_creation(self):
        """A db client can be created with the right retention policy """

        expected_retention = {
            'name': 'testRetention',
            'duration': '1h0m0s',
            'shardGroupDuration': '1h0m0s',
            'replicaN': 1,
            'default': True
        }
        assert expected_retention in self.test_client.get_list_retention_policies()

    def test_generate_a_measurement_point(self):
        """A measurement point can be created with the data specified"""

        item_name, sensor_name = ["itemA", "sensorA"]

        result = main.generate_a_measurement_point(item_name, sensor_name=sensor_name,
                                                   sensor_output_file_dir="tests/datafiles/",
                                                   output_filename="sensor_out_valid.txt")
        assert result["measurement"] == item_name
        assert result["tags"]["sensor"] == sensor_name
        assert result["fields"]["temp"] == self.expected_temp_val

    def test_write_to_db(self):
        """Writing a point to db increases the total points in the db by 1"""

        measurement, sensor_name = ["testItem", "sensorA"]
        query = f"Select * from {measurement}"

        def get_points(_query):
            """Get measurement points from db given a query"""

            try:
                return self.test_client.query(_query).raw["series"][0]["values"]
            except KeyError:
                return []

        test_point = main.generate_a_measurement_point(measurement, sensor_name=sensor_name,
                                                       sensor_output_file_dir="tests/datafiles/",
                                                       output_filename="sensor_out_valid.txt")

        original_points_in_db = get_points(query)
        main.write_data_to_db(self.test_client, [test_point])
        new_points_in_db = get_points(query)

        assert len(new_points_in_db) > len(original_points_in_db)
        assert sensor_name in str(new_points_in_db[0])
        assert str(self.expected_temp_val) in str(new_points_in_db[0])
