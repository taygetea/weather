import unittest
from weather import loadjson

__author__ = 'taygetea'


class TestLoadjson(unittest.TestCase):


    def testOne(self):
        self.response = u'you must supply a location query'
        self.url = "http://api.wunderground.com/api/dc619f36b5360543"
        print loadjson(self.url)['response']['error']['description']
        self.assertEquals(loadjson(self.url)['response']['error']['description'], self.response)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# >>> data['response']['error']
# {u'type': u'invalidquery', u'description': u'you must supply a location query'}