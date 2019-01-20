class Disjoint_set:
	def __init__(self, n):
		self.d = [i for i in range(n)]
		self.size = [ 1 for i in range(n)]

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

