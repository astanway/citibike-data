# Get the departures
json_file <- "http://abe.is/full/of/data/departures.json"
json_data <- fromJSON(paste(readLines(json_file), collapse=""))
date = names(unlist(json_data))
date = round(as.POSIXlt(as.numeric(date), origin="1970-01-01"), "hours")
values = unname(unlist(json_data))
com = data.frame(date, values)
com = xts(com[,-1], order.by=com[,1])

# Aggregate by day
departures = period.apply(com, endpoints(com, "days"), sum)

# Plot
plot(departures)

# Get the temperatures
temps = read.csv("http://abe.is/full/of/data/temps.csv", header=TRUE)
temps$datetime = round(as.POSIXct(temps$datetime), "hours")
com = data.frame(temps$datetime, temps$temp)
com = xts(com[,-1], order.by=com[,1])

#Aggregate by day
both = period.apply(com, endpoints(com, "days"), mean)

# Plot
par(new = TRUE)
plot(both, type='l', col="blue", lwd=2, ylim =c(-0, 100),xaxt="n",yaxt="n",xlab="",ylab="")
axis(4)
mtext("degrees fahrenheit",side=4,line=3)
mtext("trips",side=2,line=3)
legend("topright",col=c("black","blue"),lty=1,legend=c("departures","degrees"))

# Correlate
both = tail(both, length(departures))
merged = merge(departures, both)
ccf(drop(departures), drop(both), na.action = na.pass)
cor(merged$departures, merged$both, use='complete.obs')

# it's like 60% yo!

# Monte Carlo
rand1 = sample(nrow(departures))
rand2 = sample(nrow(both))
ccf(drop(rand1), drop(rand2), na.action = na.pass)
cor(rand1, rand2, use='complete.obs')

# it's like, nothin, yo!