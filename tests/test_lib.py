import pytest
import lib

TEST_FILE_DIR = "tests/datafiles/"


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

    @staticmethod
    def test_get_active_sensor_information_valid_info():
        """Should parse a valid sensors_info file and create data object"""

        lst_sensors = lib.get_active_sensor_information(f"{TEST_FILE_DIR}sensors_info.valid")
        assert len(lst_sensors) == 2
        assert lst_sensors[0]._fields == ('item', 'id', 'name')

    @staticmethod
    def test_get_active_sensor_information_invalid_info():
        """Should parse a invalid sensors_info file and create data object"""

        with pytest.raises(ValueError):
            lib.get_active_sensor_information(f"{TEST_FILE_DIR}sensors_info.invalid")
