#!/usr/bin/python

# weather(){ curl -s "http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=${@:-<YOURZIPORLOCATION>}"|


import urllib2
from urllib import quote
import termcolor
import argparse
import json
import asciiweather

APIKEY = 'dc619f36b5360543'
APIURL = "http://api.wunderground.com/api/" + APIKEY
parser = argparse.ArgumentParser()
parser.add_argument('time', default='now', choices=['now','tomorrow','week'])
parser.add_argument('location', nargs='+')
args = parser.parse_args()
location = ' '.join(args.location)
time = args.time

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
		newurl = loadjson(url)['location']['requesturl'][:-5] + '.json'
	except KeyError:
		return "Ambiguous query"

def forecast(locURL):
	json = loadjson(APIURL + "/forecast/q/" + locURL)
	return json['forecast']['simpleforecast']['forecastday']

def main(location, time):
	if time == "now":
		for x,y in conditions(geolookup(location)).iteritems():
			return x, y
	elif time == "tomorrow":
		return forecast(geolookup(location))[0]
	else:
		return forecast(geolookup(location))

if __name__ == "__main__":
	main(location, time)
main(location, time)
condIcon = []
highTemp = []
lowTemp = []

