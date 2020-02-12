# System imports
from datetime import datetime


class Sample(object):
    """
    Represents a sample of power meter timeseries data.
    Consists of a timestamp, kW, A, I values, as well as moving average fields.
    """
    def __init__(self, line):
        """
        Reads a timestamp in telemetry format, and parses it to python format.
        :param string line: ingested line of data in telemetry format
        """
        # Telemetry data has time, kW, V, and I fields.
        try:
            line = line.rstrip('\n')         # remove any trailing newlines
            rawfields = line.split(', ')     # four comma-separated text fields
            if len(rawfields) < 4:
                raise ValueError(f"Field count ={len(rawfields)}, must be 4")
            # Datetimes are in ISO8601 format (ex: 2018-01-08 14:54:42.630)
            # (will raise ValueError if rawfields[0] doesn't match ISO format)
            self.time = datetime.fromisoformat(rawfields[0])
            # float(str) will raise ValueError as well.
            self.kW = float(rawfields[1])
            self.V = float(rawfields[2])
            self.I_ = float(rawfields[3])

        except ValueError as ex:  # strptime doesn't match format.
            raise ValueError(f"Input line not in telemetry format: {ex}")

    def __str__(self):
        """ Return a string repr of a complete sample; see prompt.md """
        return (
            f"{self.time.isoformat(sep=' ',timespec='milliseconds') }, " +
            f"{self.kW:.3f}, " +
            f"{self.V:.3f}, " +
            f"{self.I_:.3f}, " +
            (f"{self.kW_avg:.3f}, " if hasattr(self, 'kW_avg') else ", ") +
            (f"{self.V_avg:.3f}, " if hasattr(self, 'V_avg') else ", ") +
            (f"{self.I_avg:.3f}" if hasattr(self, 'V_avg') else "")
        )

    """ VALUE ANOMALIES -- Problems with individual samples """

    def has_kW_anomaly(self):
        """ Return true if kW values < 0.0 """
        return self.kW < 0.0

    def has_V_anomaly(self):
        """ Return true if 475V < V < 485V (outside of +-5V range) """
        return (self.V < 475) or (self.V > 485)

    def has_I_anomaly(self):
        """ Return true if I values < 0.0 """
        return self.I_ < 0.0
