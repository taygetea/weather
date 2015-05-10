#!/usr/bin/python

import urllib2
from urllib import quote
import json
from math import radians, sin, cos, sqrt, asin
import sys

import asciiweather as aw


DEBUG = False
locations = dict(icon=(0, 0), nums=(23, 3), date=(26, 1))
APIKEY = 'dc619f36b5360543'
APIURL = "http://127.0.0.1"# "http://api.wunderground.com/api/" + APIKEY
icons = dict(clear=aw.clear, cloudy=aw.cloudy, partlycloudy=aw.partlycloudy, mostlycloudy=aw.partlycloudy,
             rain=aw.rainy, tstorms=aw.storm)  # TODO: make a config file with this stuff


def haversine(lat1, lon1, lat2, lon2):  # http://rosettacode.org/wiki/Haversine_formula#Python

    r = 6372.8  # Earth radius in kilometers
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1


    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))

    return r * c


def loadjson(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    data = json.loads(f.read())
    return data


def geoip():
    response = loadjson("http://ip-api.com/json")
    if response["status"] == "success":
        return response


def conditions(locurl):
    cond = loadjson(APIURL + "/conditions/q/" + locurl)
    return cond['current_observation']


def geolookup(loc):
    loc = loc.lower()
    url = APIURL + "/geolookup/q/" + quote(loc) + '.json'
    response = loadjson(url)
    if 'results' in response['response'].keys():  # Time to disambiguate!
        options = response['response']['results']
        locality = geoip()
        disambiguated = []
        strval = lambda x: {str(y) for y in x.values()}
        lc = strval(locality)
        with open("clean.json") as f:
            bigcities = json.load(f)
        for option in options:
            op = strval(option)
            if loc in bigcities.keys():
                weighted = 0
                best = []
                for entry in bigcities[loc]:
                    distance = haversine(entry['Longitude'], entry['Latitude'], locality['lat'], locality['lon'])
                    population = entry['Population']
                    if (population/distance) > weighted:
                        weighted = (population/distance)
                        best = entry
                return geolookup(' '.join([loc, best['Country']]))
            elif len(op & lc) > len(disambiguated):  # checks for raw similarity
                disambiguated = option
                return geolookup(disambiguated['zmw'])
    else:
        return loadjson(url)['location']['requesturl'][:-5] + '.json'


def forecast(locurl):
    fc = loadjson(APIURL + "/forecast/q/" + locurl)
    return fc['forecast']['simpleforecast']['forecastday']


def icon(response):
    icon = icons[response['icon']]
    return icon


def temp(response):  # TODO: check the flow of this function
    temperature = list(str(response['temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temperature)):
            row = aw.numbers[int(temperature[y])][x]
            line.append(row)
        asciitemp.append(''.join(line))
    return asciitemp


def rowbuild(rowdict):
    splitlocs = {}
    for obj in rowdict:
        xpos = rowdict[obj][0]
        ypos = rowdict[obj][1]
        for i, line in enumerate(obj):
            splitlocs[(xpos, ypos+i)] = line
    return splitlocs


def gridfill(rowdict):
    offset = max(line[0] for line in rowdict)
    width = max([x[0]+offset for x in rowdict.keys()])
    length = max([y[1] for y in rowdict.keys()]) + 1
    grid = [[" " for x in range(width)] for y in range(length)]
    for y in range(length):
        for x in range(width):
            if (x, y) in rowdict.keys():
                for index, item in enumerate(rowdict[(x, y)]):
                    grid[y][x+index] = item
    return [''.join(x) for x in grid]
# TODO: call these functions to draw the image


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('time', default='now', choices=['now','tomorrow','week'])
    # parser.add_argument('location', default='ip', nargs='+')
    # args = parser.parse_args()
    location = ' '.join(sys.argv[2:]) # ' '.join(args.location)
    time = sys.argv[1] # args.time
    print sys.argv
    if time == "now":  # TODO: move this stuff to its own time parsing function
        disp = conditions(geolookup(location))

    elif time == "tomorrow":
        disp = forecast(geolookup(location))[0]
    else:
        disp = forecast(geolookup(location))
    import pprint
    # TODO: add in the argparse stuff
    pprint.pprint(disp)