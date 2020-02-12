# System imports
from datetime import timedelta


class SampleBuffer(object):
    """
    Represents a 5-second rolling window of timeseries data Samples.
    Samples must be "appended" in chronological order to function properly.
    """
    def __init__(self,
                 duration=timedelta(seconds=5),
                 interval=timedelta(seconds=1.5)):
        """ Creates a SampleBuffer of lenght duration and max interval. """
        self.fifo = []
        self.duration = duration
        self.interval = interval

    def append(self, sample):
        # Confirm that the new sample is chronological.
        # Last sample should be before current sample.
        if len(self.fifo) > 1 and self.fifo[-1].time > sample.time:
            raise ValueError("New samples must be chronological.")
        # The internal fifo ends with the most recent sample.
        self.fifo.append(sample)
        # Clear any samples less recent than the buffer duration.
        while sample.time - self.fifo[0].time > self.duration:
            self.fifo.pop(0)    # deletes the oldest sample in buffer

    def has_time_anomaly(self, idx=-1):
        """ Return true if the latest samples are more than 1.5 secs apart """
        # Only works for two samples in a buffer.
        if len(self.fifo) < 2:
            return False
        return self.fifo[idx].time - self.fifo[idx-1].time > self.interval

    def get_window_start_time(self):
        """ A 5-second window begins 5 secs before the newest sample. """
        return self.fifo[-1].time - self.duration

    def is_contiguous(self):
        """
        SampleBuffers should only evaluate aggregations if there are no
        anomalies within the buffer.
        Return true if any Samples are anomalous, or if the buffer isn't full
        enough to provide continuous interval data.
        """
        for sample in self.fifo:  # Check for single-sample anomalies
            if (sample.has_kW_anomaly() or
                    sample.has_V_anomaly() or
                    sample.has_I_anomaly()):
                return False
        # Determine time anomalies between each sample.
        for i in range(1, len(self.fifo)):
            if self.has_time_anomaly(idx=i):    # idx checks fifo[i] vs. [i-1]
                return False

        # Finally, make sure the buffer is "full".  There isn't interval time
        # between the "window start time" and the first buffered sample.
        if self.fifo[0].time - self.get_window_start_time() > self.interval:
            return False

        return True

    def get_avg(self, key):
        """ Return an average of all samples' specified keys. """
        if key not in ['kW', 'V', 'I_']:
            raise ValueError(f"{key} is not a valid averaging field.")
        avg = 0
        try:
            for sample in self.fifo:
                avg += (sample.__getattribute__(key) / len(self.fifo))
        except Exception:     # sample's missing a field -- can't avg
            return None
        return avg
