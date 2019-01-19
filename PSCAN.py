from Graph import Graph
from GraphReader import GraphReader
from math import sqrt

class PSCAN:
    G = {}
    e = 0 # similarity threshold
    s = 0 # min num of vertex
    def __init__(self, e, s, graph, num_nodes):
        self.e = e
        self.s = s
        self.G = graph.get_dict()
        self.max_nodes = num_nodes

    def get_similarity(self, u, v):
        r_u = set()
        r_u.add(u)
        if u in self.G:
            for key in self.G[u]:
                r_u.add(key)
        
        r_v = set()
        r_v.add(v)
        if v in self.G:
            for key in self.G[v]:
                r_v.add(key)

        return len(r_u & r_v) / sqrt(len(r_u) * len(r_v))
