# run this on the server
from multiprocessing import Pool
import urllib2
import simplejson as json
from collections import defaultdict
import subprocess

url = "http://data.citibik.es/metrics/index.json"
page = urllib2.urlopen(url)
content = page.read()
stations = json.loads(content)

def process_station(station):
    departures = defaultdict(int)
    arrivals = defaultdict(int)
    available = defaultdict(int)
    try:
        print station
        if "statsd" in station:
            return
        if "velocity" in station:
            return
        if "carbon" in station:
            return
        f = "/opt/graphite/storage/whisper/" + station.replace('.','/') + ".wsp"
        raw = subprocess.Popen(["whisper-fetch.py", f, "--from=0"], stdout=subprocess.PIPE).communicate()[0]
        current = None
        for n in raw.split('\n'):
          n = n.split()
          if n[0] == "None" or n[1] == "None":
              continue
            
          if current == None:
          	  current = int(float(n[1]))

          n[0] = int(n[0])
          n[1] = int(float(n[1]))

          available[n[0]] = n[1]

          if n[1] > current:
              arrivals[n[0]] += (n[1] - current)

          if n[1] < current:
              departures[n[0]] += (current - n[1])
          current = n[1]
    except Exception as e:
        print e
        print current
        station = station.replace('.available_bikes', '-').replace('&', 'and')
        with open('arrivals/' + station + 'arrivals.csv', 'w') as outfile:
            outfile.write('datetime,arrivals\n')
            for key in sorted(arrivals.iterkeys()):
                outfile.write(str(key) + ',' + str(arrivals[key]) + '\n')
            outfile.close()

        with open('departures/' + station + 'departures.csv', 'w') as outfile:
            outfile.write('datetime,departures\n')
            for key in sorted(departures.iterkeys()):
                outfile.write(str(key) + ',' + str(departures[key]) + '\n')
            outfile.close()

        with open('available/' + station + 'available.csv', 'w') as outfile:
            outfile.write('datetime,available_bikes\n')
            for key in sorted(available.iterkeys()):
                outfile.write(str(key) + ',' + str(available[key]) + '\n')
            outfile.close()

pool = Pool()
results = pool.map(process_station, stations)
pool.close()
pool.join()
