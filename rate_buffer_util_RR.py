# -*- coding: cp936 -*-
__author__ = 'yichengliang'

#Xiang-learning by adding comments.

import csv
import sys

throughput_threshold_ratio = 0.05 #H
loss_threshold_ratio = 0.1        #L
thro_threshold = 10 / 8          #G
feedtype = 'FSL2'   #for output filename
inputfile = sys.argv[1]    #input sorted csv file by parse.py
#inputfile = 'test.txt'        
data = []   
data_to_lose = []   # dropped product number
size = 0
f = open(inputfile, 'rb')
for line in f:
    currentlist = line.split(',')
    if currentlist[0].isdigit():
        data.append((int(currentlist[0]), int(currentlist[1])))
        size += int(currentlist[0])

#append the size and arrival time on data
product_num = len(data)  # the total amount of products of this day,  N 
f.close()
throughputs = []

outputfile = feedtype + '_idle_times' + '.csv'
#writer = csv.writer(open(outputfile, 'wb', buffering=0))
#writer.writerows([('idle_start_time', 'idle_duration(ms)')])
outputfile2 = feedtype + '_throughputs.csv'
#f = open(outputfile2, 'w')
#f.write("throughput\n")

def check_throughput_ratio_inf_buffer(R): # step 1 function
    through_sum = 0
    buffered_product = []
    del throughputs[0:len(throughputs)] #empty throughput
    num_violation = 0
    time = 0
    n = 0
    j = 0
    while j < product_num:
        while j < product_num and time < int(data[j][1]):
            i = 0
            while i < len(buffered_product):
                if buffered_product[i][0] > 1428:   # Block size, remain packet of one product decrease, time is added 
                    t = 1428/(float)(R)*1000
                    time += t  # unit: ms
                    buffered_product[i][0] -= 1428
                    #print buffered_product
                else:
                    t = buffered_product[i][0]/(float(R))*1000 #when the remain packet length less than 1428, add the last transmission time
                    time += t
                    throughput = buffered_product[i][2] / (time - buffered_product[i][1])  #throughput = size of product /(departure time - arrival time) kBps
                    through_sum += throughput
                    throughputs.append(throughput)
                    if throughput < thro_threshold:  # throughput < G
                        num_violation += 1
                    buffered_product.pop(i)   #remove this product from list
                    i -= 1
                    #print buffered_product
                if j < product_num:
                    if time >= int(data[j][1]):
                        buffered_product.append([data[j][0], data[j][1], data[j][0]])
                        j += 1
                i += 1
                if len(buffered_product) == 0:  #all transmitted
                    diff = data[j][1] - time  # the time used for product j
                    #writer.writerows([(time, diff)])
                    buffered_product.append([data[j][0], data[j][1], data[j][0]])
                    time = data[j][1]
                    j += 1

        if j < product_num and len(buffered_product) == 0:
            diff = data[j][1] - time
            #writer.writerows([(time, diff)])
            buffered_product.append([data[j][0], data[j][1], data[j][0]])
            time = data[j][1]
            j += 1
        elif j < product_num:
            buffered_product.append([data[j][0], data[j][1], data[j][0]])
            time = data[j][1]
            j += 1
        else:
            print j
            break

    while len(buffered_product) != 0:
        i = 0
        while i < len(buffered_product):
            if buffered_product[i][0] > 1428:
                t = 1428/(float)(R)*1000
                time += t
                buffered_product[i][0] -= 1428
                #print buffered_product
            else:
                t = buffered_product[i][0]/(float(R))*1000
                time += t
                throughput = buffered_product[i][2] / (time - buffered_product[i][1])   #this part same as before? why?
                through_sum += throughput
                throughputs.append(throughput)
                if throughput < thro_threshold:
                    num_violation += 1
                buffered_product.pop(i)
                #print buffered_product
                i -= 1
            i += 1
    if (num_violation / float(product_num)) > throughput_threshold_ratio:   # M/N <= H equation.   num_violation is the number whose throughput < G, 
        return False
    else:
        print 'mean throughput: ' + str(through_sum / float(product_num) * 8)# calculate mean throughput by add up all throughput / amount, unit kbps.
        return True


def check_loss_ratio(R, B):               #Step2 function 
    del data_to_lose[0:len(data_to_lose)] #clear the list
    buffered_product = []                 # unidimensional
    buffered_size = 0
    num_violation = 0
    time = 0
    j = 0
    while j < product_num:
        while j < product_num and time < int(data[j][1]):
            i = 0
            while i < len(buffered_product):
                if buffered_product[i][0] > 1428:
                    t = 1428/(float)(R)*1000
                    time += t
                    buffered_product[i][0] -= 1428
                    buffered_size -= 1428
                    #print buffered_product
                else:
                    t = buffered_product[i][0]/(float(R))*1000
                    time += t
                    buffered_size -= buffered_product[i][0]  #buffered size means remain size to be sent in the program
                    buffered_product.pop(i)
                    i -= 1
                    #print buffered_product
                if j < product_num:
                    if time >= int(data[j][1]):
                        if B - buffered_size > data[j][0]:
                            buffered_product.append([data[j][0], data[j][1], data[j][0]])
                            buffered_size += data[j][0]
                        else:
                            #print 'available: ' + str(B - buffered_size) + ' ||| needed: ' + str(data[j][0])
                            data_to_lose.append(j)
                            num_violation += 1                #drop product if there is no more space
                        j += 1
                i += 1
                if len(buffered_product) == 0:
                    diff = data[j][1] - time
                    #writer.writerows([(time, diff)])
                    while j < product_num and B < data[j][0]:
                        #print 'available: ' + str(B - buffered_size) + ' ||| needed: ' + str(data[j][0])
                        data_to_lose.append(j)
                        num_violation += 1
                        j += 1
                    if j < product_num:
                        buffered_product.append([data[j][0], data[j][1], data[j][0]])
                        buffered_size += data[j][0]
                        time = data[j][1]
                        j += 1

        if j < product_num and len(buffered_product) == 0:
            diff = data[j][1] - time
            #writer.writerows([(time, diff)])
            while j < product_num and B < data[j][0]:
                #print 'available: ' + str(B - buffered_size) + ' ||| needed: ' + str(data[j][0])
                data_to_lose.append(j)
                num_violation += 1
                j += 1
            if j < product_num:
                buffered_product.append([data[j][0], data[j][1], data[j][0]])
                buffered_size += data[j][0]
                time = data[j][1]
                j += 1
        elif j < product_num:
            diff = data[j][1] - time
            #writer.writerows([(time, diff)])
            while j < product_num and B < data[j][0]:
                #print 'available: ' + str(B - buffered_size) + ' ||| needed: ' + str(data[j][0])
                data_to_lose.append(j)
                num_violation += 1
                j += 1
            if j < product_num:
                buffered_product.append([data[j][0], data[j][1], data[j][0]])
                buffered_size += data[j][0]
                time = data[j][1]
                j += 1
        else:
            print j
            break

    while len(buffered_product) != 0:
        i = 0
        while i < len(buffered_product):
            if buffered_product[i][0] > 1428:
                t = 1428/(float)(R)*1000
                time += t
                buffered_product[i][0] -= 1428
                buffered_size -= 1428
                #print buffered_product
            else:
                t = buffered_product[i][0]/(float(R))*1000
                time += t
                buffered_size -= buffered_product[i][0]
                buffered_product.pop(i)
                #print buffered_product
                i -= 1
            i += 1
    if (num_violation / float(product_num)) > loss_threshold_ratio:  # L/N <=L requirement
        return False
    else:
        print 'length of data_to_lose: ' + str(len(data_to_lose))
        print 'total number of losses: ' + str(num_violation)
        print data_to_lose[0]
        print data_to_lose[len(data_to_lose) - 1]
        return True


def lose():
    n = len(data_to_lose) - 1  
    while n >= 0:
        del data[data_to_lose[n]]    # delete the loss file from whole data
        n -= 1
    global product_num
    product_num = len(data)


def main():
    ''' Main function'''

    ''' Adjusting Rate to find the best available that satisfies the throughput threshold'''
    R = 10 * 1000000 / 8   #unit：B/s
    while check_throughput_ratio_inf_buffer(R):
        R_Mbps = R * 8 / 1000000
        print 'Rate: ' + str(R_Mbps)
        print 'Utilization: ' + str(size / float(R * 3600 * 24))
        R -= 2 * 1000000 / 8
    while not check_throughput_ratio_inf_buffer(R):
        R_Mbps = R * 8 / 1000000
        print 'Rate: ' + str(R_Mbps)
        print 'Utilization: ' + str(size / float(R * 3600 * 24))#util == size/whole days's bits
        R += 2 * 1000000 / 8
    R_Mbps = R * 8 / 1000000 # to Mb unit R
    print 'Rate: ' + str(R_Mbps)
    print 'Utilization: ' + str(size / float(R * 3600 * 24))

    ''' Decrease buffer size until the best available is found according to the loss threshold ratio'''
    B_MB = 30            #initial buffer size
    B = B_MB * 1000000   #bytes
    adjust_rate = 10     #adjust interval
    while check_loss_ratio(R, B):
        print 'Buffer size: ' + str(B_MB)
        B_MB -= adjust_rate
        B = B_MB * 1000000
    while not check_loss_ratio(R, B):
        print 'Violated!'
        print 'Buffer size: ' + str(B_MB)
        B_MB += adjust_rate
        B = B_MB * 1000000
    print 'Final buffer size: ' + str(B_MB)

    ''' Make the corresponding losses '''
    lose()

    ''' Calculate Rate again with loss'''
    while check_throughput_ratio_inf_buffer(R):
        R_Mbps = R * 8 / 1000000
        print 'Rate: ' + str(R_Mbps)
        print 'Utilization: ' + str(size / float(R * 3600 * 24))
        R -= 2 * 1000000 / 8
    while not check_throughput_ratio_inf_buffer(R):
        R += 2 * 1000000 / 8
    R_Mbps = R * 8 / 1000000
    print 'Rate: ' + str(R_Mbps)
    print 'Utilization: ' + str(size / float(R * 3600 * 24))
    #for x in throughputs:
        #f.write(str(x) + '\n')

main()
