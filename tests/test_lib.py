import lib

TEST_FILE_DIR = "tests/"


class TestLib:
    @staticmethod
    def test_get_temp_from_valid_sensor_file():
        """Should be able to read the sensor output file and return temp in float format"""

        test_file_name = "sensor_out_valid.txt"
        expected_temp_val = 29.191  # taken from the test_file
        actual_val = lib.get_temp_from_sensor(output_file_dir=TEST_FILE_DIR, output_filename=test_file_name)
        assert actual_val == expected_temp_val

    @staticmethod
    def test_get_temp_from_invalid_sensor_file():
        """Should return -1 if temp could not be read from sensor output file"""

        test_file_name = "sensor_out_invalid.txt"
        expected_temp_val = -1
        actual_val = lib.get_temp_from_sensor(output_file_dir=TEST_FILE_DIR, output_filename=test_file_name)
        assert actual_val == expected_temp_val
