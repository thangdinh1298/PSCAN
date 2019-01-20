from Graph import Graph
from GraphReader import GraphReader
from math import sqrt
from Utils import Disjoint_set
import pdb

class PSCAN:
    G = {}
    e = 0 # similarity threshold
    s = 0 # min num of vertex
    def __init__(self, e, s, graph, num_nodes):
        self.e = e
        self.s = s
        self.G = graph.get_dict()
        self.num_nodes = num_nodes


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

    def do_scan(self):
        similar_degree = [0 for i in range(self.num_nodes)]
        effective_degree = [0 if i not in self.G else len(self.G[i]) for i in range(self.num_nodes)]
        ds = Disjoint_set(self.num_nodes)
        bin_head = [-1 for i in range(self.num_nodes)]
        bin_next = [-1 for i in range(self.num_nodes)]
        max_ed = 0
        def set_ed(vertex, ed):
            nonlocal max_ed
            if ed > max_ed: max_ed = ed
            old_ed = effective_degree[vertex]
            if vertex == bin_head[old_ed]:
                bin_head[old_ed] = bin_next[vertex]
                # print("hi")
            else:
                for i, value in enumerate(bin_next):
                    if value == vertex:
                        bin_next[i] = bin_next[vertex]
            effective_degree[vertex] = ed
            if ed < 0:
                bin_next[vertex] = -1
                return
            bin_next[vertex] = bin_head[ed]
            bin_head[ed] = vertex
        
        def get_u(): #assuming no increase in ed were added
            nonlocal max_ed
            while bin_head[max_ed] == - 1 and max_ed >= 0:
                max_ed -= 1
            return -1 if max_ed < self.s else bin_head[max_ed]

        def check_core(u, computed):
            # print("Check if {} is a core: ".format(u))
            if effective_degree[u] >= self.s and similar_degree[u] < self.s:
                set_ed(u, 0 if u not in self.G else len(self.G[u]))
                similar_degree[u] = 0
                for v in self.G[u]:
                    sim = self.get_similarity(u, v)
                    # print("similarity to {} is {}".format(v, sim))
                    computed[v] = sim
                    if sim >= self.e: similar_degree[u] += 1
                    else: set_ed(u, effective_degree[u] - 1)
                    if effective_degree[v] >= 0:
                        if sim >= self.e: similar_degree[v] += 1
                        else: set_ed(v, effective_degree[v] - 1)
                    if effective_degree[u] < self.s or similar_degree[u] >= self.s:
                        break
            # print(similar_degree)
            set_ed(u, -1)

        def cluster_core(u, computed):
            for v in computed:
                if similar_degree[v] >= self.s and computed[v] >= self.e:
                    ds.union(u, v)

            for v in self.G[u]:
                if v not in computed:
                    if ds.is_connected(u, v) == False and effective_degree[v] >= self.s:
                        sim  = self.get_similarity(u, v)
                        if effective_degree[v] >= 0:
                            if sim  > self.e:
                                similar_degree[v] += 1
                            else: set_ed(v, effective_degree[v] - 1)
                        if similar_degree[v] > self.s and sim >= self.e:
                            ds.union(u, v)

        for index, value in enumerate(effective_degree): #init the bin data structure
            if value >= self.s:
                set_ed(index, value)
        print(effective_degree)
        while True:
            u = get_u()
            if u == -1: break
            computed = {}
            check_core(u, computed)
            if similar_degree[u] >= self.s:
                print(u)
                cluster_core(u, computed)

        #finished clustering core

        print(ds.d)

        #     set_ed(u, -1)
        #     print(u)
        #     print("bin_head: ",bin_head)
        #     print("bin next: ",bin_next)
        # pdb.set_trace()
        # set_ed(1, -1)
        # set_ed(4, 4)
        # print(self.G)
        # print("sim_degree: ",similar_degree)
        # print("effective degree: ",effective_degree)
        # print("bin head: ", bin_head)
        # print("bin next: ", bin_next)

gr = GraphReader("fig5.txt")
sc = PSCAN(0.6,3, gr.get_graph(), gr.num_nodes)
sc.do_scan()

# def hi():
#     a = [1,2,3,4]
#     def hello():
#         # nonlocal a
#         a[0] = 2
#     hello()
#     print(a)
# hi()