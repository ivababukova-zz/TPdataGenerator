import json
import datetime
import pprint
import random
import sys
import os
from simpleGraph import *
import scc

pp = pprint.PrettyPrinter(indent=4)

# todo from which date do I take T to start? Implement when there is more data

def removeFilename(f):
    try:
        os.remove(f)
    except OSError:
        pass

def hms_to_seconds(t):
    t = t.split(",")
    hms_index = len(t) - 1
    if len(t) > 1:
        daysNo = int(t[0].split(" ")[0])
    else:
        daysNo = 0
    h, m, s = [int(i) for i in t[hms_index].split(':')]
    return 86400*daysNo + 3600*h + 60*m + s

# find the time difference between two timestamps as a fraction of a day:
def calculateDuration(stamp1, stamp2):
    duration = int(stamp2) - int(stamp1)
    duration = hms_to_seconds(str(datetime.timedelta(seconds=duration)))
    durationFrac = duration / hms_to_seconds("24:00:00")
    return round(durationFrac, 2)

def parseConfig(config):
    with open(config, "r") as f:
        for line in f:
            conf = json.loads(line)
            if conf[0] == "m":
                m = int(conf[1])
            elif conf[0] == "n":
                n = int(conf[1])
            elif conf[0] == "d":
                d = int(conf[1])
            elif conf[0] == "T":
                T = float(conf[1])
    return(m, n, d, T)

def constructAirports(connecting, dests, hpt):
    airports = []
    with open(instanceFile, "w") as f:
        astats = ["airports", n]
        json.dump(astats, f)
        f.write("\n")
        for a in connecting:
            a.append("connecting")
            airports.append(a)
            json.dump(a, f)
            f.write("\n")
        for a in dests:
            a.append("destination")
            airports.append(a)
            json.dump(a, f)
            f.write("\n")
        for a in hpt:
            a.append("home_point")
            airports.append(a)
            json.dump(a, f)
            f.write("\n")
        json.dump(["holiday", T], f)
        f.write("\n")
        json.dump(["flights", m], f)
        f.write("\n")
    return airports

def generateA():
    A = []
    connecting = []
    dests = []
    hpt = []
    with open(allairports, "r") as f:
        for line in f:
            airport = json.loads(line)
            A.append(airport)
    with open(propsFile, "w") as f1:
        f1.write("all " + str(n) + "\n")
        # choose n airports:
        while len(connecting) < n:
            i = random.randint(0, len(A) - 1)
            f1.write(str(i) + "\n")
            a = A.pop(i)
            if a[1] == "1":
                a[1] = "0.2" # if no conn time was calculated, put default
            connecting.append(a)
        f1.write("destinations " + str(d) + "\n")
        # choose d destinations from the airports:
        while len(dests) < d:
            i = random.randint(0, len(connecting) - 1)
            f1.write(str(i) + "\n")
            dests.append(connecting.pop(i))
        # choose a home point:
        f1.write("home\n")
        i = random.randint(0, len(connecting) - 1)
        f1.write(str(i) + "\n")
        hpt.append(connecting.pop(i))
    airports = constructAirports(connecting, dests, hpt)
    return airports

def generateF(airports):
    airport_codes = [item[0] for item in airports]
    with open(fcorpus, "r") as f:
        currentDate = 0
        earliestStamp = 0
        F = []
        for line in f:
            flight = json.loads(line)
            if flight[2] in airport_codes and flight[3] in airport_codes:
                if earliestStamp == 0:
                    earliestStamp = flight[0]
                currentDate = calculateDuration(earliestStamp, flight[0])
                if currentDate + flight[1] <= T:
                    flight[0] = currentDate
                    F.append(flight)
    return F

def writeToFile(filename, items):
    with open(filename, "a") as f:
        for item in items:
            json.dump(item, f)
            f.write("\n")

def takeFromFrandomM(F):
    counter = 0
    randomF = []
    indices = []
    indices.append(["T " + str(T)])
    indices.append(["flights " + str(m)])
    while counter < m and len(F) > 0:
        i = random.randint(0, len(F) - 1)
        indices.append(str(i))
        f = F.pop(i)
        f.insert(0, counter + 1)
        randomF.append(f)
        counter += 1
    return (randomF, indices)

configFiles = sys.argv[1:]
ids = 0
numbOfFlights = 0
areStronglyConnected = False
ccsFailCounter = 0 # records how many times the current set of airports with some set of flights weren't strongly connected

for config in  configFiles:
    (m, n, d, T) = parseConfig(config)
    print(config, m, n, d, T)
    while not areStronglyConnected:
        while numbOfFlights < m or ccsFailCounter > 10:
            print("trying")
            ccsFailCounter = 0
            instanceFile = "instances/" + str(m) + "_" + str(n) + "_" + str(d) + "_" + str(int(T)) + "_" + str(ids)
            propsFile = instanceFile + "_props"
            fcorpus = "flightsCorpus"
            allairports = "airports_out"
            airports = generateA()
            F = generateF(airports)
            numbOfFlights = len(F)
        (flights, indices) = takeFromFrandomM(F)
        graph = SimpleGraph(flights, airports)
        areStronglyConnected = scc.tarjans(graph)
        ccsFailCounter += 1
    writeToFile(instanceFile, flights)
    writeToFile(propsFile, indices)
    ids += 1
    numbOfFlights = 0
