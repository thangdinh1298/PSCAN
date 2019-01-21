from math import sqrt
class Graph:
    G = {}
    def add_edge(self, source, dest, weight):
        if source not in self.G:
            self.G[source] = {dest: weight}
        else:
            self.G[source][dest] = weight

    def __str__(self):
        return "Hi"
    
    def get_dict(self):
        return self.G
    