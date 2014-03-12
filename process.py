import json

f = open('9thAve.json', 'r')
data = json.loads(f.read())[0]["datapoints"]

current = data[0][0]
arrivals = []
departures = []
for datapoint in data:
    if datapoint[0] > current:
    	arrivals.append(datapoint[1])
    elif datapoint[0] < current:
        departures.append(datapoint[1])

    current = datapoint[0]

print arrivals
print departures
