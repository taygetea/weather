
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
    num = (  # tuple(asciiweather.numbers[6])
        "   __   ",
        "  / /   ",
        " / /_   ",
        "| '_ \\  ",
        "| (_) | ",
        " \\___/  "
    )
    icon = (  # tuple(asciiweather.partlyrain)
        ".   \\_,!,_/   ,        ",
        " `.,'   __`._'_        ",
        "  /   _( =-)= = )_     ",
        "- :  (  -=  - )  =-)_  ",
        "  \\  (_-= _(    =-  _) ",
        " ,'`.-(_____-___ -__)  ",
        "'   /  / / / / / / /   ",
        "   ;   / / / / / /     "
    )
    date = tuple(["03/14/15"])
    locations = {
        num: (23, 5),
        icon: (0, 0),
        date: (23, 1)
    }

    for line in gridfill(rowbuild(locations)):
        print line