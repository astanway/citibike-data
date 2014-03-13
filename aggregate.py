# run this on the server

import urllib2
import simplejson as json
from collections import defaultdict
import subprocess

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
        f = "/opt/graphite/storage/whisper/" + station.replace('.','/') + ".wsp"
        raw = subprocess.Popen(["whisper-fetch.py", f, "--from=0"], stdout=subprocess.PIPE).communicate()[0]
        current = 0
        for n in raw.split('\n'):
          n = n.split()
          if n[0] == "None" or n[1] == "None":
              continue

          n[0] = int(n[0])
          n[1] = int(float(n[1]))

          if n[1] > current:
              arrivals[n[0]] += 1
              data[n[0]] += 1

          if n[1] < current:
              departures[n[0]] += 1
              data[n[0]] += 1
          current = n[1]
    except Exception as e:
        print e
        continue

with open('arrivals.json', 'w') as outfile:
    json.dump(arrivals, outfile)

with open('departures.json', 'w') as outfile:
    json.dump(departures, outfile)

with open('aggregated.json', 'w') as outfile:
  json.dump(data, outfile)
