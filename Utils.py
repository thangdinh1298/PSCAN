class Disjoint_set:
	def __init__(self, n):
		self.d = [i for i in range(n)]
		self.size = [ 1 for i in range(size + 1)]

	def find(self, x):
		while x != self.d[x]:
			self.d[x] = self.d[self.d[x]]
			x = self.d[x]
		return x

	def union(self, x, y):
		r_x = self.find(x)
		r_y = self.find(y)
		if r_x == r_y:
			return
		if self.size[r_x] < self.size[r_y]:
			self.DJS[r_x]= r_y
			self.size[r_y] += self.size[r_x]
		else:
			self.DJS[r_y]= r_x
			self.size[r_x] += self.size[r_y]

	def isConnected(self, x, y):
		return self.find(x) == self.find(y)

class Node:
	def __init__(self, val):
		self.val = val
		self.next = None

class Linked_list:
	def __init__(self):
		self.size = 0
		self.head = None

	def add(self, node):
		if self.size == 0:
			self.head = node
		else:
			temp = self.head
			self.head = node
			self.head.next = temp
		self.size += 1

	def remove_top(self):
		if self.is_empty():
			return None 
		temp = self.head
		self.head = self.head.next
		self.size -= 1
	def print(self):
		temp = self.head
		while temp != None:
			print(temp.val)
			temp = temp.next

	def is_empty(self):
		return self.size == 0

class Degree_manager:
	def __init__(self,  num_vertices):
		self.num_vertices = num_vertices
		self.ef_degree = [Linked_list() for i in range(self.num_vertices)] #optimization possible, set this to max deg
		self.sim_degree = [0 for i in range(self.num_vertices)] # set this to num of vertices
		self.max_ed = num_vertices - 1

	def get_top_item_with_max_ed(self):
		while self.ef_degree[self.max_ed].is_empty():
			self.max_ed -= 1
		return self.ef_degree[self.max_ed].head.val

	def decrease_ed_of_top(self):
		if self.max_ed == 0: # if already at 0 then do nuffin'
			print("effective degree can't be less than 0")

		node = self.ef_degree[self.max_ed].head
		self.ef_degree[self.max_ed].remove_top()
		self.ef_degree[self.max_ed - 1].add(node)

	def init_node_ed(self, node_num, ed):
		try:
			self.ef_degree[ed].add(Node(node_num))
		except:
			print("effective degree can't be larger than max num of vertices")

dm = Degree_manager(20)
dm.init_node_ed(5,2)
dm.init_node_ed(2,4)
dm.init_node_ed(7,2) 
dm.init_node_ed(8,4)
dm.init_node_ed(19,20)
for ll in dm.ef_degree:
	ll.print()