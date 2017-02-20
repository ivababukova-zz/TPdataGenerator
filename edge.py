class Edge:

    def __init__(self, times, arrair):
        self.arr = arrair
        self.times = [times]

    def add_time(self, t):
        self.times.append(t)
