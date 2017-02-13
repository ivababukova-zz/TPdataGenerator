import json
import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)

airports = []
dests = []
hpt = ""
T = 0

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
    global airports, dests, hpt, T
    airports = ["SOF", "AMS", "GLA", "KTW", "WAW", "EDI", "MAN"]
    dests = ["SOF", "KTW"]
    hpt = "GLA"
    T = 10
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

def generateF():
    global airports, dests, hpt, T
    with open("flightsCorpus", "r") as f:
        currentDate = 0
        earliestStamp = 0
        F = []
        for line in f:
            flight = json.loads(line)
            if flight[2] in airports and flight[3] in airports:
                if earliestStamp == 0:
                    earliestStamp = flight[0]
                currentDate = calculateDuration(earliestStamp, flight[0])
                if currentDate + flight[1] <= T:
                    flight[0] = currentDate
                    F.append(flight)
                else:
                    break

parseConfig()
generateF()
