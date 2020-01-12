from influx_measurement import InfluxMeasurement


class TestInfluxMeasurement:
    """
    Unit tests for influx_measurement.py
    """
    @staticmethod
    def test_generate_point():
        """Should generate a valid measurement object using the value provided"""

        m_val, t_val, f_val = ["mval", "tval", "fval"]
        point = InfluxMeasurement(measurement_val=m_val,
                                  tag_val=t_val,
                                  field_val=f_val).measurement_point
        assert point["measurement"] == m_val
        assert point["tags"]["sensor"] == t_val
        assert point["fields"]["temp"] == f_val

    @staticmethod
    def test_update_point():
        """Should update the default generated measurement object with a custom one"""

        test_str = "not the original val"
        inst = InfluxMeasurement("mval", "tval", "fval")
        assert inst.measurement_point != test_str
        inst.measurement_point = test_str
        assert inst.measurement_point == test_str
