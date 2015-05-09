#!/usr/bin/python

import urllib2
from urllib import quote
import json

import asciiweather as aw




# parser = argparse.ArgumentParser()
# parser.add_argument('time', default='now', choices=['now','tomorrow','week'])
# parser.add_argument('location', default='ip', nargs='+')
# args = parser.parse_args()
# ' '.join(sys.argv[1:]) # ' '.join(args.location)
# sys.argv[0] # args.time

DEBUG = False
locations = dict(icon=(0, 0), nums=(23, 3), date=(26, 1))
APIKEY = 'dc619f36b5360543'
APIURL = "http://api.wunderground.com/api/" + APIKEY
location = '34683' # TODO: arbitrary parameters
time = "now"
icons = dict(clear=aw.clear, cloudy=aw.cloudy, partlycloudy=aw.partlycloudy, mostlycloudy=aw.partlycloudy,
             rain=aw.rainy, tstorms=aw.storm) # TODO: make a config file with this stuff


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


def conditions(locURL):
    json = loadjson(APIURL + "/conditions/q/" + locURL)
    return json['current_observation']


def geolookup(loc):
    url = APIURL + "/geolookup/q/" + quote(loc) + '.json'
    response = loadjson(url)
    if 'results' in response['response'].keys():  # Time to disambiguate!
        options = response['response']['results']
        locality = geoIP()
        disambiguated = set()
        strval = lambda x: {str(y) for y in x.values()}
        lc = strval(locality)
        for option in options:
            op = strval(option)
            # TODO: check against the json
            if len(op & lc) > len(disambiguated):
                disambiguated = option
        return geolookup(disambiguated['zmw'])

    else:
        return loadjson(url)['location']['requesturl'][:-5] + '.json'


def forecast(locURL):
    json = loadjson(APIURL + "/forecast/q/" + locURL)
    return json['forecast']['simpleforecast']['forecastday']


def icon(response):
    icon = icons[response['icon']]
    return icon


def temp(response): # TODO: check the flow of this function
    temp = list(str(response['temp_f']).split('.')[0])
    asciitemp = []
    for x in range(6):
        line = []
        for y in range(len(temp)):
            row = aw.numbers[int(temp[y])][x]
            line.append(row)
        asciitemp.append(''.join(line))
    return asciitemp

# TODO: call these functions to draw the image
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
            curpos = (x, y)
            if (x, y) in rowdict.keys():
                for index, item in enumerate(rowdict[(x, y)]):
                    grid[y][x+index] = item
    return [''.join(x) for x in grid]


if __name__ == "__main__":
    if time == "now": # TODO: move this stuff to its own time parsing function
        disp = conditions(geolookup(location))
    elif time == "tomorrow":
        disp = forecast(geolookup(location))[0]
    else:
        disp = forecast(geolookup(location))
    import pprint
    # TODO: add in the argparse stuff
    pprint.pprint(disp)





