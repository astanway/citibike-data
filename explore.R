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

one = rep(c(1), length(departures))
com = data.frame(departures, one)
com = xts(com[,-1], order.by=com[,1])
departures = period.apply(com, endpoints(com, "hours"), sum)

one = rep(c(1), length(combined))
com = data.frame(combined, one)
com = xts(com[,-1], order.by=com[,1])
both = period.apply(com, endpoints(com, "hours"), sum)

plot(both)
temps = read.csv('~/code/citibike/temperatures/temps.csv')
lines(temps$datetime, temps$temp, type='l')