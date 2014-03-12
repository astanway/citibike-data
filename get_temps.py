import urllib2
import datetime
import os.path
import glob
import ujson
import apikey

PATH = '/Users/abestanway/code/citibike/temperatures/'

# Grab the data
start_date = datetime.date(2013,06,01)
end_date = datetime.date.today()
delta = datetime.timedelta(days=1)
while start_date <= end_date:
    url = 'http://api.wunderground.com/api/%s/history_YYYYMMDD/q/NY/New_York_City.json' % apikey.API_KEY
    converted = start_date.strftime('%Y-%m-%d').replace('-','')
    file_name = PATH + 'json/' + converted + '.json'

    if os.path.isfile(file_name):
        print 'already have %s' % file_name
        start_date += delta
        continue

    print 'grabbing %s' % file_name
    page = urllib2.urlopen(url.replace('YYYYMMDD', converted))
    content = page.read()
    with open(file_name, 'w') as fid:
        fid.write(content)

    start_date += delta

# Convert to csv
with open(PATH + 'temps.csv', 'w') as csv:
    csv.write('datetime,temp,humidity,windspeed,visibility,rain,snow\n')
    for fname in glob.glob(PATH + 'json/*.json'):
        with open(fname, 'r') as f:
            f = f.read().replace('-9999.0', 'NA').replace('-9999', 'NA')
            j = ujson.loads(f)
            for obs in j['history']['observations']:
                dt = '%s-%s-%s %s:%s:00' % (obs['date']['year'], obs['date']['mon'], obs['date']['mday'], obs['date']['hour'], obs['date']['min'])
                csv.write('%s,%s,%s,%s,%s,%s,%s\n' % (dt, obs['tempi'], obs['hum'], obs['wspdi'], obs['visi'], obs['rain'], obs['snow']))
