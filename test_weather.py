from unittest import TestCase
import unittest

import weather


class TestLoadjson(TestCase):
    def testOne(self):
        response = u'you must supply a location query'
        url = weather.APIURL
        self.assertEquals(weather.loadjson(url)['response']['error']['description'], response)


class TestGeoIP(TestCase):
    def testOne(self):
        geo = weather.geoip()
        self.assertEquals(geo['status'], 'success')


class TestConditions(TestCase):
    def testOne(self):
        cond = weather.conditions("10026.json")
        self.assertEquals(cond['display_location']['city'], "New York")


class TestGeolookup(TestCase):
    def testOne(self):
        loc = weather.geolookup("London")
        self.assertEquals(loc, 'global/stations/03772.json')
    def testTwo(self):
        loc = weather.geolookup("St Petersburg")
        self.assertEquals(loc, 'US/FL/Saint_Petersburg.json')




def main():
    unittest.main()

if __name__ == '__main__':
    main()
