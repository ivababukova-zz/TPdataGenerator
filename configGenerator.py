import sys
import json

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

d = sys.argv[1]
generateD2(int(d))
