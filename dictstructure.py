import asciiweather
import pprint
num = tuple(asciiweather.numbers[5])
icon = tuple(asciiweather.cloudy)
date = tuple(["03/14/15"])
locations = {
    num: (23, 5),
    icon: (0, 0),
    date: (23, 1)
}


def rowBuild(rowdict):
    splitlocs = {}
    for obj in rowdict:
        xpos = rowdict[obj][0]
        ypos = rowdict[obj][1]
        for i, line in enumerate(obj):
            splitlocs[(xpos, ypos+i)] = line
    return splitlocs

pprint.pprint(rowBuild(locations))


def gridFill():
    rowdict = rowBuild(locations)
    length = max([rowdict.keys()[1] for x in rowdict.keys()])
    grid = [[] for x in range(length)]
