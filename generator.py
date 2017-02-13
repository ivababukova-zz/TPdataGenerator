import json
import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)

airports = []
dests = []
hpt = ""
T = 0
instanceFile = ""

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
    global airports, dests, hpt, T, instanceFile
    with open("instanceConfig", "r") as f:
        for line in f:
            conf = json.loads(line)
            if conf[0] == "airports":
                airports = conf[1:]
            elif conf[0] == "destinations":
                dests = conf[1:]
            elif conf[0] == "home point":
                hpt = conf[1]
            elif conf[0] == "T":
                T = float(conf[1])
            elif conf[0] == "instanceName":
                instanceFile = conf[1]

def generateA():
    A = []
    global airports, dests, hpt
    with open("airports_out", "r") as f:
        for line in f:
            airport = json.loads(line)
            purpose = ""
            if airport[0] == hpt:
                purpose = "home_point"
            elif airport[0] in dests:
                purpose = "destination"
            elif airport[0] in airports:
                purpose = "connecting"
            if purpose != "":
                airport.append(purpose)
                A.append(airport)
    return A

def generateF():
    global airports, dests, hpt, T
    with open("flightsCorpus", "r") as f:
        currentDate = 0
        earliestStamp = 0
        F = []
        idnumb = 1
        for line in f:
            flight = json.loads(line)
            if flight[2] in airports and flight[3] in airports:
                if earliestStamp == 0:
                    earliestStamp = flight[0]
                currentDate = calculateDuration(earliestStamp, flight[0])
                if currentDate + flight[1] <= T:
                    flight[0] = currentDate
                    flight.insert(0, idnumb)
                    F.append(flight)
                    idnumb += 1
                else:
                    break
    return F

parseConfig()
F = generateF()
A = generateA()

with open(instanceFile, "w") as f:
    for airport in A:
        json.dump(airport, f)
        f.write("\n")
    for flight in F:
        json.dump(flight, f)
        f.write("\n")
