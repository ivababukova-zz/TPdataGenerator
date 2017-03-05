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

def generateD(d):
    configname = "configFiles/" + str(d) + "_D"
    n = 2 * d
    T = (d + 1) * 3
    m = 10 * d
    params = [["m, n, T are functions of d"], ["m", m], ["n", n], ["d", d], ["T", T]]
    writeToFile(params, configname)

def generateD2(d):
    configname = "configFiles/" + str(d) + "_D2"
    n = 2 * d
    T = (d + 1) * 3
    m = 14 * d
    params = [["m, n, T are functions of d"], ["m", m], ["n", n], ["d", d], ["T", T]]
    writeToFile(params, configname)

# generates m, n, d, T by a Monte Carlo simulation.
def monteCarlo():
    maxT = 31
    m = random.randint(20, 500)
    print(m)
    n = random.randint(2, 100)
    print(n)
    d = random.randint(1, maxT)
    print(d)
    T = random.randint(d, maxT)
    print(T)
# d = sys.argv[1]
# generateD(int(d))

monteCarlo()
