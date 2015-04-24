import asciiweather
num = tuple(asciiweather.numbers[5])
icon = tuple(asciiweather.partlycloudy)
date = tuple(["03/14/15"])
locdict = {
    "x": {
        10: date,
        0: icon,
        8: num
        },
    "y": {
        date: 1,
        icon: 0,
        num: 2
        }
    }

def offset(cur, orig):
    if cur - orig < 0:
        raise IndexError
    else:
        return cur - orig
grid = [[' ' for x in range(15)] for y in range(15)]
grid = []

for row in range(25):
    line = []

    for index in range(25):
        if index in locdict['x']:
            try:
                line.extend(locdict['x'][index][offset(row, locdict['y'][locdict['x'][index]])])
            except IndexError:
                pass
        else:
            line.extend(" ")
    grid.append(line)
for item in grid:
    print ''.join(item)

