There are three types of CSV files: *arrivals.csv, *departures.csv,
*available.csv. Arrivals and departures are just manipulations of the data in
available - I broke it down so you don't have to, just like I did in my blog
post. You might find http://abe.is/bucketing-event-data-in-r/ useful to further
bucket by day.

I've also included metadata.json, which includes labels (station names
corresponding to CSV file names), latitude and longitude, and nearby stations.
