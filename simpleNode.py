# node consists of name, purpose and a list of outgoing egdes. The rest props are for tarjan's

class SimpleNode:

    def __init__(self, aircode, purpose, outEdges):
        self.aircode = aircode
        self.outgoing = outEdges
        self.purpose = purpose
        # these are for the scc algorithm:
        self.visited = False
        self.index = None
        self.lowlink = None
        self.onStack = False

    def add_edge(self, edge):
        self.outgoing.append(edge)

    def visit(self):
        self.visited = True
