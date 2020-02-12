# System imports
import argparse
import sys

# Project imports
from meter_events.sample import Sample
from meter_events.sample_buffer import SampleBuffer


def process(file):
    """
    Business logic for telemetry stream processor.
    Reads input telemetry line-by-line, detects anomalies, and computes
    windowed averages of relevant fields.
    Prints processed telemetry samples and anomalies to stdout.

    :param io.IOBase file: file-like object that sources input lines.
    """
    buf = SampleBuffer()
    for line in file.readlines():
        try:
            sample = Sample(line)
            buf.append(sample)
        except ValueError:  # thrown from Sample constructor or buf.append()
            print("* Skipping non-chronological or malformed Sample...")
            continue

        # New time anomalies should be printed before the sample.
        if buf.has_time_anomaly():
            print("* Anomaly - time gap detected")
        # Load windowed averages into the sample.
        if buf.is_contiguous():
            sample.kW_avg = buf.get_avg('kW')
            sample.V_avg = buf.get_avg('V')
            sample.I_avg = buf.get_avg('I_')
        # Print the complete sample line.
        print(sample, flush=True)
        # Print any value anomalies associated with the new sample.
        if sample.has_kW_anomaly():
            print("* Anomaly - kW problem detected")
        if sample.has_V_anomaly():
            print("* Anomaly - V problem detected")
        if sample.has_I_anomaly():
            print("* Anomaly - I problem detected")


def main():
    parser = argparse.ArgumentParser(
              description="Process lines of meter telemetry data from stdin")
    parser.add_argument("-f", "--filename",
                        help="read lines from dat file, not stdin")
    args = parser.parse_args()

    # load the file.
    if args.filename:
        dat = open(args.filename)   # throws FileNotFoundError
    else:   # default to reading from stdin (realtime mode)
        dat = sys.stdin             # read lines from stdin

    process(dat)
    dat.close()


if __name__ == '__main__':
    # If we're executing as a script, throw straight into the server listening
    main()
