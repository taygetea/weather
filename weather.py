#!/usr/bin/python

import pprint

import urllib2
from urllib import quote
import argparse
import json
import asciiweather as aw

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


def draw(weather):
    icons = {u'clear': aw.clear,
             u'cloudy': aw.cloudy,
             u'partlycloudy': aw.partlycloudy,
             u'mostlycloudy': aw.partlycloudy,
             u'rain': aw.rainy}

    temp = list(str(weather[u'temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temp)):
            line.append(aw.numbers[int(temp[y])][x])
        asciitemp.append(line)
    pprint.pprint(asciitemp)
    icon = weather[u'icon']
    pprint.pprint([x for x in icons[icon]])


def main(location, time):
    if time == "now":
        weather = conditions(geolookup(location))
    elif time == "tomorrow":
        weather = forecast(geolookup(location))[0]
    else:
        weather = forecast(geolookup(location))
    return weather

if __name__ == "__main__":
    draw(main(location, time))
main(location, time)
condIcon = []
highTemp = []
lowTemp = []
