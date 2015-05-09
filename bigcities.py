import json

with open('worldcitiespop.txt') as f:
    f.next()
    cities = [city.split(',') for city in f]
    cleancities = []
    for i in cities:
        if i[4]:
            cleancities.append([i[0], i[1], int(i[4])] + [round(float(x), 1) for x in i[5:7]])
    countries = list(set([city[0] for city in cleancities]))
localcities = lambda ccode, size : [city[1:] for city in cleancities if city[0] == ccode and city[2] > size]

citydict = {}
for country in countries:

    cities = localcities(country, 100000)
    if len(cities):
        ld = []
        for city in cities:
            ld.append(dict(Name=city[0], Population=city[1], Longitude=city[2], Latitude=city[3]))
        citydict[country] = ld

with open('clean.json', 'w+') as cleaned:
    json.dump(citydict, cleaned, indent=4)