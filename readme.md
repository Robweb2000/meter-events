# Stem Meter Events
This repo is my solution to Stem's telemetry event processing design challenge (as defined in [prompt.md](prompt.md)).

## Installation and Usage
The repo is a Python3.7 package called `meter-events`.  The package is defined in [setup.py](setup.py), and can be installed using `pip install .` from the root directory.

The application can then be run as a console script as `process_meter_events`. Use the `-h` flag for detailed console script usage.

The default usage is "service mode", where telemetry lines are read one-by-one from stdin. 
`cat fixtures/telemetry.dat | process_meter_events`

It can also be used in "file mode" for batch processing: `process_meter_events -f fixtures/telemetry.dat`

## Design
The object-oriented design is straightforward. 

[sample.py](meter_events/sample.py): defines **Sample**, which encapsulates all functionality that's specific to an individual timeseries sample.
 - Parsing / deserialization from input line format
 - Serialization to output line format
 - Validation of single-sample anomalies: kW, V, I

[sample_buffer.py](meter_events/sample_buffer.py): defines **SampleBuffer**, which implements a 5-second windowed buffer of Samples.
 - Appending new samples / expiring old samples
 - Validation of chronological order
 - Detection of time anomalies
 - Calculating field averages of contiguous Samples

[\_\_main\_\_.py](meter_events/__main__.py): defines core logic of the console script.
 - `process(file)`: business logic of reading & processing lines
 - `main()`: wrapper code for console script

## Testing
Nose unit tests are defined in [test/\_\_init\_\_.py](test/__init__.py)
	 - `test_sample()`: unit test Sample functionality
	 - `test_sample_buffer()`: unit test SampleBuffer functionality

Unit tests are executed against the installed package: `python3 setup.py test`
The package is also validated to comply against PEP8 style constraints.  This is validated against the installed package: `python3 setup.py flake8`
