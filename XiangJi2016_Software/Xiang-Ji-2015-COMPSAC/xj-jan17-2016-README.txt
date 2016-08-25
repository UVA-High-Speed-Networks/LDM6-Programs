December 15th, 2015

The document shows how to generate the reusults published in COMPSAC 2015 paper.
http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7273643

scientific computing Python scripts.

List of files:
log_parser.py purpose, input, output
parse.py

ratevstime.py

rate_buffer_util.py
rate_buffer_util_RR.py

cal_meanthroughput_util_fcfs.py
cal_waiting_violation_fcfs.py

cal_meanthroughput_util_rr.py
cal_throughout_violation_rr.py

Usage: python <file.py> <argv[1]> <argv[2]>

log_parser.py and parse.py is for parsing the LDM log file.
The input file is ldmd.log. The scripts output the size, system receiving time, product creation time, latency of this product.

ratevstime.py is for processing the parsed log file with size (B) and time (ms). [MV: REFER TO FIG. in paper]
It outputs the per-min rate of feedtype product and the time index csv file. You can draw rate vs. time graph by this csv output.

rate_buffer_util.py and rate_buffer_util_RR.py is the algorithm implementation for calculating appropriate rate and buffer size based on the feedtype.
The algorithm is described in COMPSAC paper. The first scripts is FCFS mode and the second is on Round-Robin mode.

The cal scripts is calculating performance based on the post-facto rate and buffer size. The performance metrics include mean throughput and violation rate in both scenarios. 

 
