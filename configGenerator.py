import sys
import json
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

def writeToFile(data, filename):
    with open(filename, "w") as f:
        for line in data:
            json.dump(line, f)
            f.write("\n")

def generateD(configname, d):
    n = 2 * d
    T = (d + 1) * 3
    m = 10 * d
    params = [[m, n, d, T]]
    writeToFile(params, configname)

def generateD2(configname, d):
    n = 2 * d
    T = (d + 1) * 3
    m = 14 * d
    params = [[m, n, d, T]]
    writeToFile(params, configname)

# generates m, n, d, T by a Monte Carlo simulation.
def monteCarlo(configname, configNumb):
    configs = []
    for i in range(0, configNumb):
        maxT = 61
        maxN = 100
        maxM = 500
        maxD = maxT
        m = random.randint(20, maxM)
        if m < maxN:
            maxN = m
        n = random.randint(2, maxN)
        if n < maxT:
            maxD = n
        d = random.randint(1, maxD)
        T = random.randint(d, maxT)
        configs.append([m, n, d, T])
    writeToFile(configs, configname)

func = sys.argv[1]
configname = sys.argv[2]
param = sys.argv[3]

possibles = globals().copy()
possibles.update(locals())
method = possibles.get(func)

method(configname, int(param))
