#!/usr/bin/python
import urllib2
from urllib import quote
import json
from math import radians, sin, cos, sqrt, asin
import sys

import asciiweather as aw


DEBUG = False

APIKEY = 'dc619f36b5360543'
APIURL = "http://api.wunderground.com/api/" + APIKEY
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
    if locurl.startswith("/q/"):
        cond = loadjson(APIURL + "/conditions" + locurl)
    else:
        cond = loadjson(APIURL + "/conditions/q/" + locurl)
    try:
        return cond['current_observation']
    except:
        raise ValueError


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
        r = loadjson(url)

        return r['location']['l'] + '.json'

def forecast(locurl):
    fc = loadjson(APIURL + "/forecast" + locurl)
    return fc['forecast']['simpleforecast']['forecastday']


def parseresponse(r):  # TODO: check the flow of this function
    temperature = list(str(r['temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temperature)):
            row = aw.numbers[int(temperature[y])][x]
            line.append(row)
        asciitemp.append(''.join(line))
    parsed = dict(temp=tuple(asciitemp),
                  icon=tuple(icons[r['icon']]),
                  time=("Local time: " + r['local_time_rfc822'],),
                  wind=("Wind: " + r['wind_string'],),
                  humidity=("Humidity: " + r['relative_humidity'],),
                  name=(r['display_location']['full'],))
    return parsed


def rowbuild(rowdict):
    splitlocs = {}
    for obj in rowdict:
        xpos = rowdict[obj][0]
        ypos = rowdict[obj][1]
        if isinstance(type(obj), unicode):
            splitlocs[(xpos, ypos)] = obj
        else:
            for i, line in enumerate(obj):
                splitlocs[(xpos, ypos+i)] = line
    return splitlocs


def gridfill(rowdict):
    offset = max(line[0] for line in rowdict)
    width = 70
    length = max([y[1] for y in rowdict.keys()]) + 1
    grid = [[" " for x in range(width)] for y in range(length)]
    for y in range(length):
        for x in range(width):
            if (x, y) in rowdict.keys():
                for index, item in enumerate(rowdict[(x, y)]):
                    try:
                        grid[y][x+index] = item
                    except IndexError:
                        print "Index error"

    return [''.join(x) for x in grid]


def args():
    arguments = sys.argv[1:]
    for t in ["now", "tomorrow", "week", "later"]:
        if  not len(arguments):
            time = "now"
            location = "here"
        elif arguments[0] == t:
            time = arguments[0]
            location = ' '.join(arguments[1:])
        else:
            time = "now"
            location = ' '.join(arguments)
    if location == "here":
        geo = geoip()
        location = ' '.join([geo['city'], geo['region']])
    print time, location
    return time, location


if __name__ == "__main__":
    sys.argv.extend(["san", "francisco"])
    time, location = args()
    if time == "now":  # TODO: move this stuff to its own time parsing function
        disp = parseresponse(conditions(geolookup(location)))
        offsets = {disp['icon']: (0, 0), disp['temp']: (23, 1), disp['name']: (21, 0), disp['time']: (12, 9), disp['wind']: (24, 10)}
        for line in gridfill(rowbuild(offsets)):
            print line
    elif time == "tomorrow":
        geo = geolookup(location)
        print geo
        disp = parseresponse(forecast(geo)[0])
        offsets = {disp['icon']: (0, 0), disp['temp']: (23, 1), disp['name']: (21, 0), disp['time']: (23, 9), disp['wind']: (24, 10)}
    else:
        disp = forecast(geolookup(location))

    # TODO: add in the argparse stuff
