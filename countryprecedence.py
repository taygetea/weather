from collections import Counter
import pprint
from operator import itemgetter

print "loading file..."
cities = open('worldcitiespop.txt')
cities.next()
citylist = ()
done = 0
print "file has %d lines" % sum(1 for line in cities)
for city in cities:
    city = city.split(',')
    if city[4]:
        country = city[0]
        name = city[1]
        popul = int(city[4])
        lat = round(float(city[5]), 2)
        long = round(float(city[6]), 2)
        citylist = citylist + (country, name, popul, lat, long)
        done += 1
        print "%d cities done" % done
citylist = sorted(citylist, key=itemgetter(3))
print "done."





pprint.pprint([i for i in citylist if i[3] > 1999999])

print "done"

duplicates = Counter(citylist).most_common(10)[2]
print duplicates
quit()
uniquecities = set([city[1] for city in citylist])

commoncities = {}
for disambcity in list(uniquecities):


    # countries[country] = [citylist[i] for i in range(len(citylist)) if country in citylist[i][0]]
    largest = []
    for city1 in citylist:
        if city1[1] == disambcity and citylist.count(disambcity) > 1:
            print city1[1], city1[0]
            if not largest:
                largest = city1
            if city1[3] > largest[3]:
                commoncities[disambcity] = tuple(largest)
                largest = city1





# pprint.pprint(commoncities)