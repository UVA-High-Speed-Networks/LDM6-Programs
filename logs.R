library(e1071)
data <- read.csv("~/Desktop/IDSldmd.log.csv")
attach(data)

#Summary of size 
summary(product_size)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#39     128     168    1424     308 2779000 

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
hist(product_size,xlim=c(0,5000),ylim=c(0,150000),las=0,breaks=20000, xlab="Bytes", main = "Whole size range")

#Top 75 percentile range histogram x=(0,308)
hist(product_size,xlim = c(10,308),ylim = c(0,30000),las=0,breaks=200000,xlab="Byte",main="Top 75 Perentile of size range")
#Count
sum(product_size<308)
#221672

---------------------------------
#Summary of latency
summary(latency.ms.)
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#21.0   101.0   160.0   891.9   313.0 59870.0 

#Percentiles
quantile(latency.ms., c(.25, 0.5, 0.75))
#25% 50% 75% 
#101 160 313 

#Skewness of Size
print(moment(latency.ms., order=3, center=TRUE)/(sd(latency.ms.)^3))
#9.175761

#CV of Size
print(sd(latency.ms.)/mean(latency.ms.))
#5.463127

#Latency histogram 
hist(latency.ms.,las=0, xlim=c(0,2000),breaks = 2000, xlab="ms", main = "Whole latency range")

#Top 75 percentile range histogram x=(0,313)
hist(latency.ms.,xlim = c(10,313),las=0,breaks=5000,xlab="Byte",main="Top 75 Perentile of latency range")
#Count
sum(product_size<1424)
#267644




