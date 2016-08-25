##Xiang Ji modify Yicheng's code to calculate mean throughput for products
##
##Last updated: Sep.21 2014




import csv
import sys



feedtype = 'NEXRAD2'
data = []
size = 0
inputfile = sys.argv[1]
f = open(inputfile, 'rb')
for line in f:
    currentlist = line.split(',')
    if currentlist[0].isdigit():   #ignore the first line
        data.append((int(currentlist[0]), int(currentlist[1])))  # append the size and the time into data []
        size += int(currentlist[0]) #whole day size

product_num = len(data)  # total products number

def my_range(start, end, step):  # define rate range.
    while start <= end:
        yield start      #the results from generator are stored
        start += step

        
def missed_deadline(R, W, B):
 ## print R
    if B == [0]:
        return False
    waiting_times = []
    for i in range(0, len(B)):
        w_i = B[i] / R  # waiting time for product i
        waiting_times.append(w_i)    # make the list of all product's waiting time
    waiting_times.sort()  # sort the list 
    if waiting_times[int(0.80 * len(waiting_times))] > W:  # if 80% wi > W
        return False
    return True

outputfile = feedtype + '_utilization_80_percentile_waiting_time' + '.csv'
writer = csv.writer(open(outputfile, 'wb', buffering=0))
writer.writerows([('Waiting_time', 'rate', 'Buffer_size', 'utilization', 'Mean throughput')])  # write results into the table

for Waiting_time in my_range(1, 2, 1):  # waiting time range 15-20, step is 0.5
    rate = 10 * 1000000 / 8  #unit:B/s  10's unit is Mbps
    buffer_sizes = [0]
    current_ratio = missed_deadline(rate, Waiting_time, buffer_sizes)
    for i in range(1, len(data)):
        b = max(0, buffer_sizes[len(buffer_sizes) - 1] + data[i - 1][0] - rate * (data[i][1] - data[i - 1][1]) / float(1000))
        buffer_sizes.append(b) # used buffered size 
    Buffer_size = max(buffer_sizes) / 1000000   # choose the biggest buffer size as B
    current_ratio = missed_deadline(rate, Waiting_time, buffer_sizes) # Print R
    while(not current_ratio): # while false, rate is too small, so increase the rate
        rate += 10 * 1000000 / 8   #Unit Mbps
        buffer_sizes = [0]
        for i in range(1, len(data)):
            b = max(0, buffer_sizes[len(buffer_sizes) - 1] + data[i - 1][0] - rate * (data[i][1] - data[i - 1][1]) / float(1000))
            buffer_sizes.append(b)
        Buffer_size = max(buffer_sizes) / 1000000
        current_ratio = missed_deadline(rate, Waiting_time, buffer_sizes)   # check and print R
    #current_ratio = missed_deadline(rate, Waiting_time, buffer_sizes)
    if (current_ratio):           # while true, rate is okay ,so decrease the rate by  for a better utilization
        while(current_ratio):
            rate = rate - 2 * 1000000 / 8
            buffer_sizes = [0]
            for i in range(1, len(data)):
                b = max(0, buffer_sizes[len(buffer_sizes) - 1] + data[i - 1][0] - rate * (data[i][1] - data[i - 1][1]) / float(1000))
                buffer_sizes.append(b)
            Buffer_size = max(buffer_sizes) / 1000000
            current_ratio = missed_deadline(rate, Waiting_time, buffer_sizes)  # if too small , than plus 2
        rate += 2 * 1000000 / 8    # result R
        print 'rate:' +str(rate * 8 / 1000000)
        buffer_sizes = [0]
        for i in range(1, len(data)):
            b = max(0, buffer_sizes[len(buffer_sizes) - 1] + data[i - 1][0] - rate * (data[i][1] - data[i - 1][1]) / float(1000))
            buffer_sizes.append(b)   
        Buffer_size = max(buffer_sizes) / 1000000 #result B
        waiting_times = []
        for i in range(0, len(buffer_sizes)):
            w_i = buffer_sizes[i] / rate
            waiting_times.append(w_i)  # waiting time list
            
        throughputs = [0]
	through_sum = 0
        for i in range(0,len(buffer_sizes)):
            throughput = data[i][0] / (waiting_times[i] + (data[i][0] / float(rate)))  #B/s
            throughputs.append(throughput)

        
        through_sum = sum(throughputs)
	utilization = float(size) / (rate * 3600 * 24)  # corresponding utilization  
	print 'util:'+str(utilization)
	mean_throughput = (through_sum / float(product_num) * 8) #bps
	print 'meanthrou:' +str(mean_throughput)
	writer.writerows([(Waiting_time * 1000, rate * 8 / 1000000, Buffer_size, utilization, mean_throughput)])
    throughputs_output = feedtype + 'throughput of waiting time' + str(Waiting_time) + '.csv'
    writer2 = csv.writer(open(throughputs_output, 'wb', buffering=0))
    writer2.writerows([('Throughput', '')])
    for x in throughputs:
        writer2.writerows([(x, '')])




