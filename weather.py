#!/usr/bin/python


import urllib2
from urllib import quote
import argparse
import json
import asciiweather as aw

DEBUG = False
WIDTH = 80
ICONPOS = [0, 0]
NUMPOS = [23, 3]
locations = {'icon': (0, 0),
             'nums': (23, 3),
             'date': (26, 1)}
APIKEY = 'dc619f36b5360543'
APIURL = "http://api.wunderground.com/api/" + APIKEY
parser = argparse.ArgumentParser()
# parser.add_argument('time', default='now', choices=['now','tomorrow','week'])
# parser.add_argument('location', nargs='+')
args = parser.parse_args()
location = "34683"  # ' '.join(args.location)
time = "now"  # args.time


def loadjson(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    data = json.loads(f.read())
    return data


def conditions(locURL):
    json = loadjson(APIURL + "/conditions/q/" + locURL)
    return json['current_observation']


def geolookup(loc):
    url = APIURL + "/geolookup/q/" + quote(loc) + '.json'
    try:
        return loadjson(url)['location']['requesturl'][:-5] + '.json'
    except KeyError:
        return "Ambiguous query"


def forecast(locURL):
    json = loadjson(APIURL + "/forecast/q/" + locURL)
    return json['forecast']['simpleforecast']['forecastday']


def draw(weather={'temp_f': 47.6, 'icon': 'partlycloudy'},
         iconpos=ICONPOS, numpos=NUMPOS):
    icons = {'clear': aw.clear,
             'cloudy': aw.cloudy,
             'partlycloudy': aw.partlycloudy,
             'mostlycloudy': aw.partlycloudy,
             'rain': aw.rainy,
             'tstorms': aw.storm}
    icon = icons[weather['icon']]
    temp = list(str(weather['temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temp)):
            row = aw.numbers[int(temp[y])][x]
            line.append(row)
        asciitemp.append(''.join(line))
    return asciitemp, icon
    # for x in asciitemp:
    #     print x
    # for x in range(len(icon)):
    #     print str(icon[x])


def main(location, time):
    if time == "now":
        weather = conditions(geolookup(location))
    elif time == "tomorrow":
        weather = forecast(geolookup(location))[0]
    else:
        weather = forecast(geolookup(location))
    return weather

if __name__ == "__main__":
    if DEBUG:
        draw()
    else:

        draw(main(location, time))

condIcon = []
highTemp = []
lowTemp = []
