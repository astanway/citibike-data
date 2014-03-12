import urllib2
import simplejson as json
from collections import defaultdict

url = "http://data.citibik.es/metrics/index.json"
page = urllib2.urlopen(url)
content = page.read()
stations = json.loads(content)
arrivals = defaultdict(int)
departures = defaultdict(int)
data = defaultdict(int)
for station in stations:
    try:
        print station
        if "statsd" in station:
            continue
        if "velocity" in station:
            continue
        if "carbon" in station:
            continue
        url = "http://data.citibik.es/render/?from=20130614&format=json&target=" + station.replace('&', '%26')
        page = urllib2.urlopen(url)
        content = page.read()
        j = json.loads(content)
        current = 0
        for n in j[0]['datapoints']:
          if n[0] == None:
              continue

          if int(n[0]) > current:
              arrivals[n[1]] += int(n[0])
              data[n[1]] += int(n[0])

          if int(n[0]) < current:
              departures[n[1]] += int(n[0])
              data[n[1]] += int(n[0])

          current = int(n[0])
          print current
    except:
        continue

with open('arrivals.json', 'w') as outfile:
    json.dump(arrivals, outfile)

with open('departures.json', 'w') as outfile:
    json.dump(departures, outfile)

with open('aggregated.json', 'w') as outfile:
  json.dump(data, outfile)