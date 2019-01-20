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
		temp.next = None
		print("removed ", temp)
	def print(self):
		temp = self.head
		while temp != None:
			print(temp.val, " ", end="")
			temp = temp.next

	def is_empty(self):
		return self.size == 0

class Degree_manager:
	def __init__(self,  num_vertices):
		self.num_vertices = num_vertices
		self.ef_degree = [0 for i in range(self.num_vertices)] #optimization possible, set this to max deg
		self.sim_degree = [0 for i in range(self.num_vertices)] # set this to num of vertices
		self.buckets = [Linked_list() for i in range(self.num_vertices)]
		self.max_ed = -1

	def increment_sd(self, vertex):
		self.sim_degree[vertex] += 1		

	def init_node_ed(self, node_num, ed):
		try:
			self.buckets[ed].add(Node(node_num))
			self.ef_degree[node_num] = ed
			if ed > self.max_ed:
				self.max_ed = ed
		except:
			print("effective degree can't be larger than max num of vertices")

	def set_sd(self, node_num, sd):
		self.sim_degree[node_num] = sd

	def set_ed(self, node_num, ed):
		old_ed = self.ef_degree[node_num]
		if self.buckets[old_ed].is_empty(): #empty when initialize
			pass
		#remove from bucket 
		if self.buckets[old_ed].head.val == node_num:
			self.buckets[old_ed].remove_top()
		else:
			node = self.buckets[old_ed].head
			while node.next.val != node_num:
				node = node.next
			temp = node.next
			node.next = temp.next
			temp.next = None
		# add to new bucket
		self.buckets[ed].add(Node(node_num))
		#update ef_degree
		ef_degree[node_num] = ed

	def get_ed(self, vertex):
		return self.ef_degree[vertex]

	def get_sd(self, vertex):
		return self.sim_degree[vertex]


	def get_top_item_with_max_ed(self):
		# print(self.max_ed)
		return self.buckets[self.max_ed].head.val

	def decrement_ed_of_top(self):
		if self.max_ed == 0: # if already at 0 then do nuffin'
			print("effective degree can't be less than 0")

		node = self.buckets[self.max_ed].head
		# print("top val is: ", node.val)
		# print("node value is: ", node.val)
		self.buckets[self.max_ed].remove_top()
		self.buckets[self.max_ed - 1].add(node)
		if self.buckets[self.max_ed].is_empty():
			self.max_ed -= 1
		# decrease in ef_degree array
		self.ef_degree[node.val] -= 1
