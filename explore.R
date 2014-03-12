dat = read.csv("http://data.citibik.es/render/?from=-1weeks&target=9-Ave-%26-W-22-St.available_bikes&format=csv", header=TRUE)
dat = setNames(dat, c("station", "date", "bike"))
dat$date = as.POSIXct(dat$date)
current = 1
arrivals = c()
departures = c()
combined = c()
for (i in 1:length(dat$date)) {
  n = dat$bike[i]
  if(is.na(n)){
    next
  }
  if (n > current) {
    arrivals = append(arrivals, dat$date[i])
    combined = append(combined, dat$date[i])
  }
  if (n < current) {
    departures = append(departures, dat$date[i])
    combined = append(combined, dat$date[i])
  }
  current = n
}

# ! HOW TO BUCKET EVENT DATA !

one = rep(c(1), length(arrivals))
com = data.frame(arrivals, one)
com = xts(com[,-1], order.by=com[,1])
arrivals = period.apply(com, endpoints(com, "hours"), sum)

# Get the trips
json_file <- "~/code/citibike/departures.json"
json_data <- fromJSON(paste(readLines(json_file), collapse=""))
date = names(unlist(json_data))
date = as.POSIXlt(as.numeric(date), origin="1970-01-01")
values = unname(unlist(json_data))
com = data.frame(date, values)
com = xts(com[,-1], order.by=com[,1])
departures = period.apply(com, endpoints(com, "days"), sum)
plot(departures)

# Plot the temps
par(new = TRUE)
temps = read.csv("~/code/citibike/temperatures/temps.csv", header=TRUE)
temps$datetime = as.POSIXct(temps$datetime)
com = data.frame(temps$datetime, temps$temp)
com = xts(com[,-1], order.by=com[,1])
both = period.apply(com, endpoints(com, "days"), mean)
plot(both, type='l', col="blue", lwd=2, ylim =c(-0, 100),xaxt="n",yaxt="n",xlab="",ylab="")
axis(4)
mtext("degrees",side=4,line=3)
mtext("trips",side=2,line=3)
legend("topright",col=c("black","blue"),lty=1,legend=c("trips","degrees"))


# Correlate
ccf(drop(departures), drop(both), na.action = na.pass)

# Monte Carlo
rand1 = sample(nrow(departures))
rand2 = sample(nrow(both))
ccf(drop(rand1), drop(rand2), na.action = na.pass)
cor(rand1, rand2, use = "pairwise.complete.obs")