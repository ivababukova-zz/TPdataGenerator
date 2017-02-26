# Given:
#   - the _props file with the random numbers
#   - flights corpus
#   - all airports
# generates the same instance that was generated once by generator.py
# In order to have reproducible instances functionality.

import datetime
import sys
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

def getBasicParams():
    with open(props, "r") as f:
        for line in f.readlines():
            line = line.split()
            if len(line) == 2:
                if line[0] == "T":
                    T = float(line[1])
                elif line[0] == "all":
                    n = int(line[1])
                elif line[0] == "destinations":
                    d = int(line[1])
                elif line[0] == "flights":
                    m = int(line[1])
                elif line[0] == "startStamp":
                    startStamp = int(line[1])
    return(m, n, d, T, startStamp)

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
    with open(props, "r") as f:
        for line in f.readlines():
            airport = line.split()
            if airport[0] == "T" or airport[0] == "flights":
                turn = ""
            elif airport[0] == "all" or airport[0] == "destinations" or airport[0] == "home":
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

def generateF(airports, T, startStamp):
    airport_codes = [item[0] for item in airports]
    with open(fcorpus, "r") as f:
        currentDate = 0
        earliestStamp = 0
        F = []
        for line in f:
            flight = json.loads(line)
            if flight[2] in airport_codes and flight[3] in airport_codes and flight[0] >= startStamp:
                if earliestStamp == 0:
                    earliestStamp = flight[0]
                currentDate = calculateDuration(earliestStamp, flight[0])
                if currentDate + flight[1] <= T:
                    flight[0] = currentDate
                    F.append(flight)
    return F

def takeFromF():
    F = generateF(A, T, startStamp)
    counter = 0
    with open(props, "r") as f1, open(regFile, "a") as f2:
        json.dump(["holiday", T], f2)
        f2.write("\n")
        json.dump(["flights", m], f2)
        f2.write("\n")
        turn = ""
        for numb in f1.readlines():
            numb = numb.split()
            if numb[0] == "startStamp":
                turn = numb[0]
            elif turn == "startStamp":
                counter += 1
                numb = int(numb[0])
                flight = F.pop(numb)
                flight.insert(0, counter)
                json.dump(flight, f2)
                f2.write("\n")

instanceName = sys.argv[1]

fcorpus = sys.argv[2]
allairports = "airports_out"
props = "props/" + instanceName + "_props"
regFile = "instances/" + instanceName

(m, n, d, T, startStamp) = getBasicParams()

A = regenerateA()
takeFromF()
