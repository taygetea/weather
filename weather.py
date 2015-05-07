#!/usr/bin/python


import urllib2
from urllib import quote
import argparse
import json
import asciiweather as aw
import drawascii
import sys


DEBUG = False

locations = {'icon': (0, 0),
             'nums': (23, 3),
             'date': (26, 1)}
APIKEY = 'dc619f36b5360543'
APIURL = "http://api.wunderground.com/api/" + APIKEY

# parser = argparse.ArgumentParser()
# parser.add_argument('time', default='now', choices=['now','tomorrow','week'])
# parser.add_argument('location', default='ip', nargs='+')
# args = parser.parse_args()
location = "new york"  # ' '.join(sys.argv[1:]) # ' '.join(args.location)
time = "now"  # sys.argv[0] # args.time

print time, location
def loadjson(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    data = json.loads(f.read())
    return data


def geoIP():
    response = loadjson("http://ip-api.com/json")
    if response["status"] == "success":
        return response
    else:
        raise LookupError


def conditions(locURL):
    json = loadjson(APIURL + "/conditions/q/" + locURL)
    return json['current_observation']


def geolookup(loc):
    print APIURL
    print quote(loc)
    url = APIURL + "/geolookup/q/" + quote(loc) + '.json'
    response = loadjson(url)
    if 'results' in response['response'].keys():
        options = response['response']['results']
        locality = geoIP()
        disambiguated = set()
        for option in options:
            strval = lambda x: {str(y) for y in x.values()}
            op = strval(option)
            lc = strval(locality)
            if len(op & lc) > len(disambiguated):
                disambiguated = option
        print disambiguated

    else:
        return loadjson(url)['location']['requesturl'][:-5] + '.json'



def forecast(locURL):
    json = loadjson(APIURL + "/forecast/q/" + locURL)
    return json['forecast']['simpleforecast']['forecastday']


def icon(weather):
    icons = {'clear': aw.clear,
             'cloudy': aw.cloudy,
             'partlycloudy': aw.partlycloudy,
             'mostlycloudy': aw.partlycloudy,
             'rain': aw.rainy,
             'tstorms': aw.storm}
    icon = icons[weather['icon']]
    return icon


def temp(weather):
    temp = list(str(weather['temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temp)):
            row = aw.numbers[int(temp[y])][x]
            line.append(row)
        asciitemp.append(''.join(line))
    return asciitemp


if __name__ == "__main__":
    if time == "now":
        weather = geolookup(location)
    elif time == "tomorrow":
        weather = forecast(geolookup(location))[0]
    else:
        weather = forecast(geolookup(location))
    import pprint
    pprint.pprint(weather)








condIcon = []
highTemp = []
lowTemp = []
