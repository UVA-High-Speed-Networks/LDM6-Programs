############################################################
#Author: Xiang Ji
#Usage: python calculate mean throughput and util for calibration
# verify the result

######################### NOTE #############################
#
############################################################

import csv
import sys

R = int(raw_input("Please enter the rate: ")) * 1000000 / 8
B = int(raw_input("Please enter the buffer size: ")) * 1000000
    
thro_threshold = 10 / 8 #unit: kBps
throughput_threshold_ratio = 0.05

inputfile = sys.argv[1]    #input csv file
        
data = []   
data_to_lose = []   # list of dropped product number because space not enough in buffer
data_violation = [] # list of dropped product number because too small throughput (throughtput violation), something like QoS guarantee

size = 0

f = open(inputfile, 'rb')
for line in f:
    currentlist = line.split(',')
    if currentlist[0].isdigit():
        data.append((int(currentlist[0]), int(currentlist[1])))
        size += int(currentlist[0])
                         
product_num = len(data)  
f.close()
throughputs = []



def cal_violation():
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
                    time += t
                    buffered_product[i][0] -= 1428
                    #print buffered_product
                else:
                    t = buffered_product[i][0]/(float(R))*1000 #when the remain packet length less than 1428, add the last transmission time
                    time += t
                    throughput = buffered_product[i][2] / (time - buffered_product[i][1])  #throughput = size of product /(departure time - arrival time)
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
            print j #total number after loss 
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
                throughput = buffered_product[i][2] / (time - buffered_product[i][1])   
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
        print 'mean throughput: ' + str(through_sum / float(product_num) * 8)
        print 'Utilization: ' + str(size / float(R * 3600 * 24))
        return True
    

def main():
    
    cal_violation()
    
    
main()
