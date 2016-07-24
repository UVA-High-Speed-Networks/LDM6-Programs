library(e1071)
data <- read.csv("~/Desktop/Test/HRS/HDSldmdSorted.log.csv")
attach(data)

--------------------
#Summary of size 
summary(product_size)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#39    4574    9348   15000   10380 2261000 

#Percentiles
quantile(product_size, c(.25, .50, .75))
#25%   50%   75% 
#4574  9348 10384 

#Skewness of Size
print(moment(product_size, order=3, center=TRUE)/(sd(product_size)^3))
#18.7349

#CV of Size
print(sd(product_size)/mean(product_size))
#2.260773

#Size histogram 
hist(product_size,las=0,ylim=c(0,300000),breaks=200, xlab="Bytes", main = "Whole size range")

#Top 75 percentile range histogram x=(0,10384)
hist(product_size,xlim = c(10,10384),ylim = c(0,100000),las=0,breaks=10000,xlab="Byte",main="Top 75 Perentile of size range")
#Count
sum(product_size<10384)
#292437

---------------------------------
#Summary of latency
summary(latency.ms.)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#20     364    3354   76020   19760 3537000 

#Percentiles
quantile(latency.ms., c(.25, 0.5, 0.75))
#25%   50%   75% 
#364  3354 19761  

#Skewness of Size
print(moment(latency.ms., order=3, center=TRUE)/(sd(latency.ms.)^3))
#5.971463

#CV of Size
print(sd(latency.ms.)/mean(latency.ms.))
#3.731045

#Latency histogram 
hist(latency.ms.,las=0,breaks = 50, xlab="ms", main = "Whole latency range")

#Top 75 percentile range histogram x=(0,19761)
hist(latency.ms.,xlim = c(0,19761),las=0,breaks=15000,xlab="Byte",main="Top 75 Perentile of latency range")

#Count
sum(product_size<19761)
#331762




