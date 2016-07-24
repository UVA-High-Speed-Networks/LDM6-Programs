######################## LDM FEEDTYPE Log File Parser  ##############################
# Usage: python inputfile feedtype
# Example: python ldmd.log NEXRAD2
# Author: Zihan Ni
# Email: zn8ae@virginia.edu
################################################################################


import csv
import sys

from datetime import datetime, timedelta

##A function to convert the time string to datetime object than calculate the time difference, it consider the received time is UTC time - 5:00
##Sample convert: a = datetime.strptime("2014-11-18T09:20:44.404740-05:00","%Y-%m-%dT%H:%M:%S.%f-05:00")
##Sample convert: b = datetime.strptime("20141118142043.687","%Y%m%d%H%M%S.%f")

# a function that calculates the time difference in minutes
# between two time stamps.
def latency(a, b):
	s1 = a
	s2 = b
	FMT1 = "%Y-%m-%dT%H:%M:%S.%f-04:00"
	FMT2 = "%Y%m%d%H%M%S.%f"
	difference = datetime.strptime(s2, FMT1) + timedelta(hours = 4) - datetime.strptime(s1, FMT2)

	#A timedelta object has days, seconds, microseconds. Convent to miliseconds
        return (difference.days * 24 * 3600 * 1000000 + difference.seconds * 1000000 + difference.microseconds) / 1000

def time_difference(a, b):
	s1 = a + '000'
	s2 = b + '000'
	FMT = '%Y%m%d%H%M%S.%f'
	difference = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
	return (difference.days * 24 * 3600 * 1000000 + difference.seconds * 1000000 + difference.microseconds) / 1000


# the input file name is set by command line parameter
inputfile = sys.argv[1]

# the type name is set by command line parameter
feedtype = sys.argv[2]

# create or open csv file for writing
# appends to the same feed type csv file
outputfile = feedtype + inputfile + '.csv'
writer = csv.writer(open(outputfile, 'wb', buffering=0))
writer.writerows([('product_size','time_difference', 'create_time', 'receive_time','latency(ms)')])


f = open(inputfile, 'r')

initial_time = ""
tdifference = 0
counter = 0


for line in f:
    currentlist = line.split()
    #determine if the line contains data
    if currentlist[4].isdigit():
        #determine and process first data
        if initial_time == "":
            initial_time = currentlist[5]
        
        rectime = (currentlist[0])
        cretime = (currentlist[5])
        tdifference = time_difference(initial_time, cretime)
        delay = abs(latency(cretime, rectime)) #Fix negative problem.
        writer.writerows([(int(currentlist[4]), int(tdifference), str(currentlist[5]),str(currentlist[0]),int(delay))])
f.close()




