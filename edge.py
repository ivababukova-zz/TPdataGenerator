class Edge:

    def __init__(self, times, arrair):
        self.arr = arrair
        self.times = times
        self.isVisited = False

    def add_time(self, t):
        self.times.append(t)
