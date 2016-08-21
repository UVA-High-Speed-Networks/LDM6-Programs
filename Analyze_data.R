library(e1071)
data <- read.csv("~/Desktop/IDSsorted.log.csv")
attach(data)

#Summary of size 
summary(product_size)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#39     128     168    1424     308   2779000 

#Percentiles
quantile(product_size, c(.25, .50, .75))
#30% 50% 70% 
#134 168 259 

#Skewness of Size
print(moment(product_size, order=3, center=TRUE)/(sd(product_size)^3))
#133.0719

#CV of Size
print(sd(product_size)/mean(product_size))
#10.46955

#Size histogram 
hist(product_size,las=0, xlab="Bytes", main="")

#Top 75 percentile range histogram x=(0,308)
hist(product_size,xlim = c(0,308),las=0,breaks=100000,xlab="Byte",main="")
#Count
sum(product_size<308)
#221672

#Inter-arrival Time
---------------------------------
#Summary of inter-arrival time
summary(int_time)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#0.00    0.00    0.00   79.74    1.00 7587.00 

#Percentiles
quantile(int_time, c(.25, 0.5, 0.75))
#25% 50% 75% 
#0   0   1 

#Skewness of inter-arrival time
print(moment(int_time, order=3, center=TRUE)/(sd(int_time)^3))
#6.442993

#CV of inter-arrival time
print(sd(int_time)/mean(int_time))
#4.829775

#inter-arrival time histogram 
hist(int_time, xlab="Milliseconds",main = "")

#Top 75 percentile range histogram x=(0,1)
hist(int_time,main = "", xlab="Milliseconds",xlim=c(0,1),breaks=100000)

#Count
#295585




