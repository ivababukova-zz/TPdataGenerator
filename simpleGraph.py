from simpleEdge import *
from simpleNode import *

import pprint
pp = pprint.PrettyPrinter(indent=4)

# graph consists of:
    # list of destinations
    # home point
    # list of connecting airports
# all of which are nodes

class SimpleGraph:
    # create a graph for given lists of airports and flights:
    def __init__(self, flights, airports):
        self.alln = []
        for airport in airports:
            node = SimpleNode(airport[0], airport[2], [])
            self.alln.append(node)

        for flight in flights:
            dep = self.get_node(flight[3])
            arr = self.get_node(flight[4])
            outgoing = dep.outgoing
            existing = False
            for e in outgoing:
                if e.arr == arr:
                    existing = True
                    break
            if not existing:
                edge = SimpleEdge(arr)
                dep.add_edge(edge)

    def get_node(self, airconntime):
        for node in self.alln:
            code = node.aircode
            if code == airconntime:
                return node

    def print_graph(self):
        for node in self.alln:
            print("from ", node.aircode, " to:")
            for edge in node.outgoing:
                print(edge.arr.aircode)
            print("*****")
