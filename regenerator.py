# Given:
#   - the instance config
#   - the _aprops and _fprops files with the random numbers
#   - flights corpus
#   - all airports
# generates the same instance that was generated once by generator.py
# In order to have reproducible instances functionality.

import datetime
import sys
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

instanceName = sys.argv[1]

config = "instanceConfig"
fcorpus = "flightsCorpus"
allairports = "airports_out"
fprops = instanceName + "_fprops"
aprops = instanceName + "_aprops"
regFile = instanceName + "_re"
m = 0
T = 0

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

def parseConfig():
    global T, m, n, d
    with open("instanceConfig", "r") as f:
        for line in f:
            conf = json.loads(line)
            if conf[0] == "T":
                T = float(conf[1])
            if conf[0] == "m":
                m = int(conf[1])

def readAllAirports():
    global allairports
    A = []
    with open(allairports, "r") as f:
        for line in f:
            airport = json.loads(line)
            A.append(airport)
    return A

def regenerateA():
    allairps = []
    conns = []
    dests = []
    hpt = []
    turn = ""
    A = readAllAirports()
    with open(aprops, "r") as f:
        for line in f.readlines():
            airport = line.split()
            if airport[0] == "all" or airport[0] == "destinations" or airport[0] == "home":
                turn = airport[0]
            elif turn == "all":
                a = A.pop(int(airport[0]))
                if a[1] == "1":
                    a[1] = "0.2" # if no conn time was calculated, put default
                conns.append(a)
                allairps.append(a)
            elif turn == "destinations":
                dests.append(conns.pop(int(airport[0])))
            elif turn == "home":
                hpt.append(conns.pop(int(airport[0])))
    with open(regFile, "w") as f:
        astats = ["airports", len(allairps)]
        json.dump(astats, f)
        f.write("\n")
        for a in conns:
            a.append("connecting")
            json.dump(a, f)
            f.write("\n")
        for a in dests:
            a.append("destination")
            json.dump(a, f)
            f.write("\n")
        for a in hpt:
            a.append("home_point")
            json.dump(a, f)
            f.write("\n")
    return allairps

def generateF(airports, T):
    airport_codes = [item[0] for item in airports]
    with open("flightsCorpus", "r") as f:
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

def takeFromF():
    F = generateF(A, T)
    counter = 0
    with open(fprops, "r") as f1, open(regFile, "a") as f2:
        json.dump(["holiday", T], f2)
        f2.write("\n")
        json.dump(["flights", m], f2)
        f2.write("\n")
        for numb in f1.readlines():
            counter += 1
            numb = int(numb.split()[0])
            flight = F.pop(numb)
            flight.insert(0, counter)
            json.dump(flight, f2)
            f2.write("\n")

parseConfig()
A = regenerateA()
takeFromF()
