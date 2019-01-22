from Graph import Graph
from GraphReader import GraphReader
from math import sqrt, ceil
from Utils import Disjoint_set
import sys

class PSCAN:
    G = {}
    e = 0 # similarity threshold
    s = 0 # min num of vertex
    def __init__(self, e, s, graph, num_nodes):
        self.e = e
        self.s = s
        self.G = graph.get_dict()
        self.num_nodes = num_nodes
        for i in range(self.num_nodes):
            if i not in self.G:
                self.G[i] = {i : 0.0}
            else:
                self.G[i][i] = 0.0


    # def get_similarity(self, u, v):
    #     r_u = set()
    #     r_u.add(u)
    #     if u in self.G:
    #         for key in self.G[u]:
    #             r_u.add(key)
        
    #     r_v = set()
    #     r_v.add(v)
    #     if v in self.G:
    #         for key in self.G[v]:
    #             r_v.add(key)

    #     # print("len {} is {}, len {} is {}, len u&v is {}".format(u, len(r_u), v, len(r_v), len(r_u&r_v)))
    #     return len(r_u & r_v) / sqrt(len(r_u) * len(r_v))

    def check_structure_simmilar(self, u, v):
        cn_u_v = ceil(self.e * sqrt(len(self.G[u]) * len(self.G[v])))

        cn = 0
        for x in self.G[u]:
            if x in self.G[v]:
                cn += 1
                if cn >= cn_u_v:
                    return True
        return False

    def do_scan(self):
        similar_degree = [0 for i in range(self.num_nodes)]
        effective_degree = [len(self.G[i]) for i in range(self.num_nodes)]
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
            # if u == 8:
            #         print(effective_degree[u])
            if effective_degree[u] >= self.s and similar_degree[u] < self.s:
                set_ed(u, len(self.G[u])) # since we're not looping through u itself, preinitialize sd and ed to be 2
                similar_degree[u] = 0
                for v in self.G[u]:
                    is_sim = self.check_structure_simmilar(u, v)
                    computed[v] = is_sim
                    if is_sim == True: similar_degree[u] += 1
                    else: set_ed(u, effective_degree[u] - 1)
                    if effective_degree[v] >= 0:
                        if is_sim == True: similar_degree[v] += 1
                        else: set_ed(v, effective_degree[v] - 1)
                    if effective_degree[u] < self.s or similar_degree[u] >= self.s:
                        break
            set_ed(u, -1)

        def cluster_core(u, computed):
            for v in computed:
                if similar_degree[v] >= self.s and computed[v] == True:
                    ds.union(u, v)

            for v in self.G[u]:
                if v not in computed:
                    if ds.is_connected(u, v) == False and effective_degree[v] >= self.s:
                        is_sim  = self.check_structure_simmilar(u, v)
                        if effective_degree[v] >= 0:
                            if is_sim  == True:
                                similar_degree[v] += 1
                            else: set_ed(v, effective_degree[v] - 1)
                        if similar_degree[v] > self.s and is_sim == True:
                            ds.union(u, v)

        def cluster_non_core():
            for v in range(self.num_nodes):
                if similar_degree[v] >= self.s:
                    root = ds.find(v)
                    clusters[root].append(v)
                    cid[v].append(root)

            for index ,cluster in enumerate(clusters):
                if len(cluster) > 0:
                    cluster_copy = set(cluster)
                    for u in cluster_copy:
                        for v in self.G[u]:
                            if similar_degree[v] < self.s and v not in cluster_copy:
                                is_sim = self.check_structure_simmilar(u, v)
                                if is_sim == True:
                                    cluster.append(v)
                                    cid[v].append(index)
            for cluster in clusters:
                if len(cluster) > 0:
                    print("Cluster includes: ",set(cluster))

        # def detect_hub_and_outlier():
        #     for v, id in enumerate(cid):
        #         if len(id) == 0: # is a non_member
        #             is_bridge = False
        #             for x in self.G[v]:
        #                 if is_bridge == True:
        #                     break
        #                 for y in self.G[v]:
        #                     if x != y: 
        #                         is_bridge = check_bridge(v, x, y)
        #                         if is_bridge == True:
        #                             break
        #             if is_bridge == False:
        #                 outliers.append(v)

        # def check_bridge(v, x, y):
        #     if len(cid[x]) == 0 or len(cid[y]) == 0: # if cid[x] = 0 OR cid[y] = 0 then outlier
        #         return False
        #     else:
        #         for i in cid[x]:
        #             if i not in cid[y]: #is a hub
        #                 hubs.append(v)
        #                 return True
        #         for j in cid[y]:
        #             if j not in cid[x]: #is a hub
        #                 hubs.append(v)
        #                 return True
        #     return False

        def detect_hub_and_outlier():
            for v, id in enumerate(cid):
                if len(id) == 0: # is a non_member
                    if is_hub(v):
                        hubs.append(v)
                    else:
                        outliers.append(v)

        def is_hub(v):
            for i in range(len(clusters)):
                for j in range(i+1, len(clusters)):
                    if is_bridge(v, clusters[i], clusters[j]):
                        return True

            return False

        def is_bridge(v, clustera, clusterb):
            for x in self.G[v]:
                for y in self.G[v]:
                    if x != y and x != v and y != v:
                        if x in clustera and y in clusterb:
                            return True
            return False    

        for index, value in enumerate(effective_degree): #init the bin data structure
            if value >= self.s:
                set_ed(index, value)
        # print(bin_head)
        # print(bin_next)
        while True:
            u = get_u()
            if u == -1: break
            computed = {}
            check_core(u, computed)
            if similar_degree[u] >= self.s:
                # print(u)
                cluster_core(u, computed)

        # print(similar_degree)
        clusters = [[] for i in range(self.num_nodes)]
        cid = [[] for i in range(self.num_nodes)]
        cluster_non_core()
        #finished clustering core
        hubs = []
        outliers = []
        detect_hub_and_outlier()
        print("Hubs are:", hubs)
        print("Outliers are:", outliers)
        # print(ds.d)

# Graph trong bai xiaowei lay tham so la 0.677 va 4


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage PSCAN.py <filename> <epsilon> <mu>")
        exit()
    filename = sys.argv[1]
    epsilon = float(sys.argv[2])
    mu = int(sys.argv[3])

    gr = GraphReader(filename)
    sc = PSCAN(epsilon, mu, gr.get_graph(), gr.num_nodes)
    sc.do_scan()