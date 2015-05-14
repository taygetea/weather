import json


"""
This code cleans the city data from here, and puts it into a JSON file if the city has a population over
some threshold. This is used to create a heuristic as to what is meant when a user inputs the name of a city.

"""

threshold = 100000

with open('worldcitiespop.txt') as f:
    f.next()
    cities = [city.split(',') for city in f]
    cleancities = []
    for i in cities:
        if i[4]:
            cleancities.append([i[0], i[1], int(i[4])] + [round(float(x), 2) for x in i[5:7]])
    countries = list(set([city[0] for city in cleancities]))
    cityset = list(set([city[1] for city in cleancities]))
localcities = lambda cc, size: [x for x in cleancities if x[0] == cc and x[2] > size]

citydict = {}

for country in countries:
    cities = localcities(country, threshold)
    if len(cities):
        for city in cities:
            singlecity = dict(Country=city[0], Population=city[2], Longitude=city[3], Latitude=city[4])
            if city[1] not in citydict.keys():
                citydict[city[1]] = [singlecity]
            else:
                citydict[city[1]].append(singlecity)
                print city[1]



with open('clean.json', 'w+') as cleaned:
    json.dump(citydict, cleaned, indent=4, sort_keys=True)