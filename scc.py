import pprint
pp = pprint.PrettyPrinter(indent=4)

from simpleGraph import *

flights = [
[1, 17.49, 0.14, "LBA", "BTS", 19.99],
[2, 59.49, 0.14, "LBA", "BTS", 24.74],
[3, 35.0, 0.06, "BTS", "LBA", 16.99],
[4, 48.84, 0.14, "LBA", "BTS", 21.86],
[5, 45.65, 0.06, "BTS", "LBA", 20.99],
[6, 63.0, 0.06, "BTS", "LBA", 24.74],
[7, 24.49, 0.14, "LBA", "BTS", 16.49],
[8, 17.65, 0.06, "BTS", "LBA", 14.99],
[9, 14.0, 0.06, "BTS", "LBA", 16.49],
[10, 49.0, 0.06, "BTS", "LBA", 22.49],
[11, 10.49, 0.14, "LBA", "BTS", 9.99],
[12, 52.65, 0.06, "BTS", "LBA", 21.86],
[13, 28.0, 0.06, "BTS", "LBA", 16.49],
[14, 45.49, 0.14, "LBA", "BTS", 24.99],
[15, 31.49, 0.14, "LBA", "BTS", 16.99]
]

airports = [
["BTS", "0.36", "connecting"],
["NCE", "0.03", "destination"],
["LBA", "0.22", "home_point"]
]

def strongconnect(v, indx, S, graph, CCs):
    v.index = indx
    v.lowlink = indx
    indx += 1
    S.append(v.aircode)
    v.onStack = True

    for edge in v.outgoing:
        w = edge.arr
        if w.index is None:
            strongconnect(w, indx, S, graph, CCs)
            v.lowlink = min(v.lowlink, w.lowlink)
        elif w.onStack:
            v.lowlink = min(v.lowlink, w.index)

    if v.lowlink == v.index:
        cc = []
        codes = S[:]
        for code in codes:
            node = graph.get_node(code)
            if node.lowlink == v.lowlink:
                S.remove(code)
                cc.append(code)
        CCs.append(cc)

def hasSolutions(graph, CCs):
    mustbevisited = set([a.aircode for a in graph.alln if a.purpose == "home_point" or a.purpose == "destination"])
    pp.pprint(mustbevisited)
    for cc in CCs:
        if mustbevisited.issubset(set(cc)):
            return True
    return False


def tarjans(graph):
    indx = 1
    S = []
    CCs = []
    for v in graph.alln:
        if v.index is None:
            strongconnect(v, indx, S, graph, CCs)
    if len(S) > 0:
        CCs.append(S[:])
    pp.pprint(CCs)
    return hasSolutions(graph, CCs)
