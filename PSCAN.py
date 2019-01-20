from Graph import Graph
from GraphReader import GraphReader
from math import sqrt
from Utils import Disjoint_set

class PSCAN:
    G = {}
    e = 0 # similarity threshold
    s = 0 # min num of vertex
    def __init__(self, e, s, graph, num_nodes):
        self.e = e
        self.s = s
        self.G = graph.get_dict()
        self.num_nodes = num_nodes
        self.dm = Degree_manager(self.num_nodes)
        self.ds = Disjoint_set(self.num_nodes)

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


    def check_core(self, vertex):
        if self.dm.get_ed(vertex) >= self. s and self.dm.get_sd < self.s:
            self.dm.set_ed(vertex, 0 if vertex not in self.G else len(G[vertex]) )
            self.dm.set_sd(vertex, 0)
            for v in G[vertex]:
                sim = self.get_similarity(vertex, v)
                if sim >= self.e:
                    self.dm.increment_sd(vertex)
                else:
                    decrement

    def do_scan(self):
        # explored = [False for i in range(self.num_nodes)]
        # #init effective degree
        # for vertex in range(self.num_nodes):
        #     self.dm.init_node_sd(vertex, 0)
        #     if vertex in G:
        #         self.dm.init_node_ed(vertex, len(G[vertex]))
        #     else:
        #         self.dm.init_node_ed(vertex, 0)

        # #phase 1
        # i = 1
        # while i <= self.num_nodes:
        #     vertex = self.dm.get_top_item_with_max_deg()
        #     if explored[vertex] == False:
        #         self.check_core(vertex)
        #         if self.dm.get_sd(vertex) >= self.s:
        #             self.cluster_core(u)
        #         i += 1
        similar_degree = [0 for i in range(self.num_nodes)]
        effective_degree = [0 if i not in self.G else len(G[i]) for i in range(self.num_nodes)]
        ds = Disjoint_set(self.num_nodes)
        bin_head = [-1 for i in range(self.num_nodes)]
        bin_next = [-1 for i in range(self.num_nodes)]
        max_ed = 0
        for index, value in effective_degree:
            if value >= s:
                ed = value
                if ed > max_ed:
                    max_ed = ed
                bin_next[index] = bin_head[ed]
                bin_head[ed] = index

        while True:
            u = -1