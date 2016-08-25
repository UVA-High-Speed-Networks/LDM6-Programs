######################## LDM notifyme Log File Parser  ##############################
# This Python program parses an LDM log file that is generated
# by a downstream LDM process using notifyme command, and generates
# a csv file that records the size of each received product at the 
# relevate time
#
# Usage:
#			python parse.py LOG_FILE_NAME FEED_TYPE
#
# Example:
#			python parse.py data.txt NGRID
#
#
# Author: Yicheng Liang   
# Email: yl9jv@virginia.edu
# Modified by: Xin Song (xs4gs@virginia.edu)
######################################################################################


import csv
import sys
from datetime import datetime


# a function that calculates the time difference in minutes
# between two time stamps.
# Be careful when parsing something with a creation time at the end of the month
# cannot do date 31 to date 01 conversion
def time_difference(a, b):
	s1 = a + '000'
	s2 = b + '000'
	FMT = '%Y%m%d%H%M%S.%f'
	difference = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
	return (difference.days * 24 * 3600 * 1000000 + difference.seconds * 1000000 + difference.microseconds) / 1000

# the type name is set by command line parameter
typename = sys.argv[2]
# the input file name is set by command line parameter
inputfile = sys.argv[1]

# create or open csv file for writing
# appends to the same feed type csv file
outputfile = typename + '.csv'
#outputfile2 = typename + '_rate.csv'   
writer = csv.writer(open(outputfile, 'wb', buffering=0))
writer.writerows([('size', 'arrival_time', 'post_inter-arrival_time')])  # appended 'date' and 'previous_timestamp' columns
# writer2 = csv.writer(open(outputfile2, 'wb', buffering=0))
# writer2.writerows([('size', 'arrival_time', 'post_inter-arrivel_time', 'rate')])

# read data file line by line for parsing
with open(inputfile, 'r') as f:  # use the "with" statement to automately close the file safely
	initial_time = ""
	difference = 0
	current_difference = 0
	previous_size = 0
	previous_arrival = 0
	previous_sum = 0
	post_interval = 0
	interval_sum = 0
	counter = 0
	previous_date = ""
	previous_timestamp = ""

	for line in f:
		currentlist = line.split()
		# Determine if this line contains data
		if currentlist[5].isdigit():
			if initial_time == "": # for the first valid data entry
				initial_time = currentlist[6]
				previous_size = currentlist[5]
				previous_arrival = currentlist[6]
				previous_sum = int(currentlist[5]) # accumulative sum of product sizes
				previous_date = currentlist[0]+currentlist[1]+"_"+currentlist[2] # in the form of "Jun 01 00:12:05"
				previous_timestamp = repr(currentlist[6])
			else:
				difference = time_difference(initial_time, previous_arrival) # is 0 when executed the first time
				current_difference = time_difference(initial_time, currentlist[6]) # is the actual inter-arrival time
				post_interval = current_difference - difference
				interval_sum += post_interval # can be used as the arrival time for next product
				writer.writerows([(previous_size, difference, post_interval)]) # this is the main written line
				# if current_difference == difference:
				# 	previous_sum += int(currentlist[5]) # size? previous_sum is only used for writer2 for rate
				# else:
				# 	writer2.writerows([(previous_sum, difference, post_interval, float(previous_sum) / post_interval * 8 / 1000)])
				# 	previous_sum = int(currentlist[5])
				# 	counter += 1
				previous_size = currentlist[5]
				previous_arrival = currentlist[6]
				previous_date = currentlist[0]+currentlist[1]+"_"+currentlist[2]
				previous_timestamp = repr(currentlist[6])

	#average_interval = interval_sum / counter
	#writer.writerows([(previous_size, current_difference, average_interval)]) # ('size', 'arrival_time', 'inter-arrival_time')
	# writer2.writerows([(previous_sum, current_difference, average_interval, float(previous_sum) / average_interval)])#('size', 'arrival_time', 'inter-arrivel_time', 'rate')		


