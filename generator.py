import json
import datetime
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

airports = []
T = 0
instanceFile = "instances/test"
fFile = instanceFile + "_fprops"
aFile = instanceFile + "_aprops" # saves all data required to generate instanceFile again
m = 0
n = 0
d = 0

# from which date do I take T to start?

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
    global airports, dests, hpt, T, m, n, d
    with open("instanceConfig", "r") as f:
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

def constructAirports(connecting, dests, hpt):
    global airports
    for a in connecting:
        a.append("connecting")
        airports.append(a)
    for a in dests:
        a.append("destination")
        airports.append(a)
    for a in hpt:
        a.append("home_point")
        airports.append(a)

def generateA():
    global n, d
    A = []
    connecting = []
    dests = []
    hpt = []
    with open("airports_out", "r") as f:
        for line in f:
            airport = json.loads(line)
            A.append(airport)
    with open(aFile, "w") as f1:
        f1.write("randomly chosen airports:\n")
        # choose n airports:
        while len(connecting) < n:
            i = random.randint(0, len(A) - 1)
            f1.write(str(i) + "\n")
            a = A.pop(i)
            if a[1] == "1":
                a[1] = "0.2" # if no conn time was calculated, put default
            connecting.append(a)
        f1.write("randomly chosen destinations:\n")
        # choose d destinations from the airports:
        while len(dests) < d:
            i = random.randint(0, len(connecting) - 1)
            f1.write(str(i) + "\n")
            dests.append(connecting.pop(i))
        # choose a home point:
        f1.write("randomly chosen home point:\n")
        i = random.randint(0, len(connecting) - 1)
        f1.write(str(i) + "\n")
        hpt.append(connecting.pop(i))
    constructAirports(connecting, dests, hpt)

def generateF():
    global airports, T, fFile
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

def takeFromFrandomM():
    global m, instancePropsFile
    counter = 0
    F = generateF()
    with open(fFile, "w") as f1, open(instanceFile, "a") as f2:
        f1.write("randomly chosen flights:\n")
        while counter < m and len(F) > 0:
            i = random.randint(0, len(F) - 1)
            f1.write(str(i) + "\n")
            f = F.pop(i)
            f.insert(0, counter + 1)
            json.dump(f, f2)
            f2.write("\n")
            counter += 1


parseConfig()
generateA()

with open(instanceFile, "w") as f:
    astats = []
    astats.append("airports")
    astats.append(n)
    json.dump(astats, f)
    f.write("\n")
    for airport in airports:
        json.dump(airport, f)
        f.write("\n")
    json.dump(["holiday"], f)
    f.write("\n")
    json.dump(T, f)
    f.write("\n")
    fstats = ["flights", m]
    json.dump(fstats, f)
    f.write("\n")

takeFromFrandomM()
