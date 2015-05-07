from collections import Counter
import json
import pprint
from sys import stdout
import time

print "loading file..."
cities = open('worldcitiespop.txt')

citylist = []
for city in cities[1:]:
    citylist.append(city.split(','))
print "done."


print "removing unpopulated, \r%d to check" % len(citylist)
j = 0
tempcities = []
for i, city in enumerate(citylist):
    if city[4]:
        tempcities.append(i)
    else:
        j = j + 1
    stdout.write("removing unpopulated, \r%d to check, \r%d duplicates found" % (len(citylist), j))
    stdout.flush()
stdout.write("\n")

print "done"

numcountries = set([city[0] for city in citylist])
done = 0
countries = {}
for country in numcountries:
    stdout.write("creating dictionary, \r{0:d}".format(len(numcountries) - done) + " out of %d" % len(numcountries))
    stdout.flush()
    countries[country] = [citylist[i] for i in range(len(citylist)) if country in citylist[i][0]]
    done = done + 1
stdout.write("\ndone")

pprint.pprint(countries['mt'])