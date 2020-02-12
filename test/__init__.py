"""
# Unit tests

"""
# System imports
from datetime import datetime, timedelta

# 3rd party imports
import nose

# Project imports
from meter_events.sample import Sample
from meter_events.sample_buffer import SampleBuffer

VALID_INPUT_LINE = "2018-01-08 14:54:42.630, 441.781, 477.470, 925.254"


def test_sample():
    """ Validates parsing, manipulation, and string conversion of Sample """
    sample = Sample(VALID_INPUT_LINE)

    assert sample.time == datetime(2018, 1, 8, 14, 54, 42, 630000)
    # Validate proper field mapping
    assert sample.kW == 441.781
    assert sample.V == 477.470
    assert sample.I_ == 925.254

    # There should be no field anomalies.
    assert not sample.has_kW_anomaly()
    assert not sample.has_V_anomaly()
    assert not sample.has_I_anomaly()

    # Print to string, and validate output format (including aggregates).
    assert str(sample) == VALID_INPUT_LINE + ", , , "

    # Add sample averages, and validate output format.
    sample.kW_avg = 369.123
    sample.V_avg = 456.172
    sample.I_avg = 1.234
    assert str(sample) == VALID_INPUT_LINE + ", 369.123, 456.172, 1.234"

    # Changing fields to invalid values should trigger anomalies.
    sample.kW = -0.001      # negative power anomaly
    assert sample.has_kW_anomaly()
    sample.V += 10          # over-voltage anomaly
    assert sample.has_V_anomaly()
    sample.V -= 15          # under-voltage anomaly
    assert sample.has_V_anomaly()
    sample.I_ = -0.001      # negative current anomaly
    assert sample.has_I_anomaly()


def test_sample_buffer():
    """ Validates Sample buffering fuctionality -- time gaps and averages """
    buf = SampleBuffer()
    first = Sample(VALID_INPUT_LINE)
    buf.append(first)

    second = Sample(VALID_INPUT_LINE)
    second.time += timedelta(seconds=1)
    buf.append(second)
    assert not buf.has_time_anomaly()   # 1 second interval -- less than 1.5s

    # Generate a contiguous buffer by adding 5 samples with 1-sec intervals.
    third = Sample(VALID_INPUT_LINE)
    third.time += timedelta(seconds=2)
    buf.append(third)
    fourth = Sample(VALID_INPUT_LINE)
    fourth.time += timedelta(seconds=3)
    buf.append(fourth)

    assert not buf.is_contiguous()

    fifth = Sample(VALID_INPUT_LINE)
    fifth.time += timedelta(seconds=4)
    buf.append(fifth)

    assert buf.is_contiguous()
    # Calculate 5-second averages.
    assert buf.get_avg('kW') == 441.781
    assert buf.get_avg('V') == 477.470
    assert buf.get_avg('I_') == 925.254

    # Introduce "discontinuities" in time and value.
    buf = SampleBuffer()
    buf.append(first)
    buf.append(second)
    # missing third sample!
    buf.append(fourth)
    buf.append(fifth)
    assert not buf.is_contiguous()

    # Try a value discontinuity.
    third.V = 473.15
    assert third.has_V_anomaly()
    buf = SampleBuffer()
    buf.append(first)
    buf.append(second)
    buf.append(third)
    buf.append(fourth)
    buf.append(fifth)
    assert not buf.is_contiguous()


nose.main()
