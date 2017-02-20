from edge import *

class Node:

    def __init__(self, aircode, airconntime, purpose, outEdges):
        self.aircode = aircode
        self.airconntime = airconntime
        self.outgoing = outEdges
        self.purpose = purpose
        self.isVisited = False

    def add_edge(self, edge):
        self.outgoing.append(edge)

    def visit(self):
        self.visited = True
