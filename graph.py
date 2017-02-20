from edge import *
from node import *

import pprint
pp = pprint.PrettyPrinter(indent=4)

# graph consists of:
    # list of destinations
    # home point
    # list of connecting airports
# all of which are nodes

class Graph:
    # create a graph for given lists of airports and flights:
    def __init__(self, flights, airports):
        self.alln = []
        self.startn = []
        for airport in airports:
            node = Node(airport[0], float(airport[1]), airport[2], [])
            self.alln.append(node)
            if airport[2] == "home_point":
                self.startn.append(node)

        for flight in flights:
            dep = self.get_node(flight[3])
            arr = self.get_node(flight[4])
            times = [float(flight[1]), float(flight[1]) + float(flight[2])]
            outgoing = dep.outgoing
            existing = False
            for edge in outgoing:
                if edge.arr.aircode == arr.aircode:
                    edge.add_time(times)
                    existing = True
                    break
            if not existing:
                edge = Edge(times, arr)
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
                print(edge.arr.aircode, edge.times, )
            print("*****")


flights = [
[1, 1, 0.1, "SOF", "GLA", 62.15],
[2, 0, 0.1, "GLA", "SOF", 44.4],
[3, 2, 0.1, "GLA", "SOF", 79.21],
[4, 4, 0.1, "EDI", "SOF", 21.59],
[5, 3, 0.1, "EDI", "GLA", 50.88],
[6, 5, 0.1, "EDI", "SOF", 190.04],
[7, 6, 0.24, "SOF", "EDI", 59.59],
[8, 7, 0.13, "EDI", "GLA", 41.38]
]

airports = [
["SOF", "0.01", "destination"],
["EDI", "0.01", "connecting"],
["GLA", "0.01", "home_point"]]

graph = Graph(flights, airports)
graph.print_graph()
