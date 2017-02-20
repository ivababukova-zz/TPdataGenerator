import pprint
pp = pprint.PrettyPrinter(indent=4)

from simpleGraph import *

# def dfs(s, counter):
#     print(s.aircode)
#     s.visit()
#     for edge in s.outgoing:
#         n = edge.arr
#         if not n.visited:
#             counter += 1
#             dfs(n, counter)
#
# def DFS(graph):
#     dfs(graph.alln[0], 1)

flights = [
[1, 0, 0.1, "1", "2", 62.15],
[2, 0, 0.1, "2", "3", 44.4],
[3, 0, 0.1, "3", "4", 79.21],
[4, 0, 0.1, "4", "5", 21.59],
[5, 0, 0.1, "5", "6", 50.88],
[6, 0, 0.1, "6", "3", 190.04],
[7, 0, 0.24, "1", "7", 59.59],
[8, 0, 0.13, "7", "2", 41.38],
[9, 0, 0.13, "7", "8", 41.38]
]

airports = [
["1", "0.01", "destination"],
["2", "0.01", "connecting"],
["3", "0.01", "connecting"],
["4", "0.01", "connecting"],
["5", "0.01", "connecting"],
["6", "0.01", "connecting"],
["7", "0.01", "connecting"],
["8", "0.01", "home_point"]
]

def strongconnect(v):
    global indx, S
    v.index = indx
    v.lowlink = indx
    indx += 1
    S.append(v.aircode)
    v.onStack = True

    for edge in v.outgoing:
        w = edge.arr
        if w.index is None:
            strongconnect(w)
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

graph = SimpleGraph(flights, airports)
indx = 1
S = []
CCs = []
for v in graph.alln:
    if v.index is None:
        strongconnect(v)

CCs.append(S[:])

pp.pprint(CCs)
