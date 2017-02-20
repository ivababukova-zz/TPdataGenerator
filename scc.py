import pprint
pp = pprint.PrettyPrinter(indent=4)
from simpleGraph import *

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
