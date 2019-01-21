from Graph import Graph
class GraphReader:
    G = Graph()
    num_nodes = 0
    def __init__(self, filename):
        file = open(filename, "r")
        self.num_nodes = int(file.readline())
        for line in file:
            line = line.split()
            source = int(line[0])
            dest = int(line[1])
            weight = float(line[2])
            self.G.add_edge(source, dest, weight)
    
    def get_graph(self):
        return self.G

# f = GraphReader("graph_out.txt")
# f = f.get_graph()
# for key in f:
#     print(f[key])