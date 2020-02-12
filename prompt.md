# Interview project

Provide object-oriented system design, implementation, and test plan for the
following requirements:

  * Read telemetry in from the attached data file in the format

  ```
  T, kW, V, I
  ```

  * For each of the kW, V, and I fields, process the input data and output a log in the following format:

  ```
T, kW, V, I, kW-avg, V-avg, I-avg
  ```

  where the first four fields are the input values for each timestamp and the avg fields are the 5-second sliding window average of the corresponding input field (i.e. only output averages when there are no gaps in the data for the last five seconds).

  * Detect anomalies in the input data and output a line describing the anomaly

  ```
2018-01-08 14:54:42.630, 441.781, 477.470, 925.254, , ,
2018-01-08 14:54:43.784, 320.249, 475.942, 672.873, , ,
2018-01-08 14:54:44.900, 435.929, 482.613, 903.268, , ,
2018-01-08 14:54:46.010, 357.977, 475.937, 752.151, , ,
2018-01-08 14:54:47.189, 461.782, 483.066, 955.939, 403.544, <remaining values>
...
<time>, <kW>, <V>, <I>, <kW-avg>, <V-avg>, <I-avg>
* Anomaly - time gap detected
<time>, <kW>, <V>, <I>, , ,
  ```

  Anomalies to detect:
    * Time gaps greated than 1.5 seconds between inputs
    * kW values < 0.0
    * V values outside range of 480 V +/- 5.0 V
    * I values < 0.0
