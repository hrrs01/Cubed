
import sys
import re
class Cubed:
	def __init__(self):
	
		self.file = None
		self.commands = []
		self.stack = [0]
		
		self.index = -1
		
		self.loop_start = [0]
		
		self.stack_index = 0
		self.functions = {"[": self.loop, "]": self.loop_end, "+": self.add, "-": self.sub, ".": self.output, "<": self.left, ">": self.right, ",": self.input, "^": self.append_code, "~": self.open_file}
		
		
	def add(self):
		
		self.stack[self.stack_index] += 1
		if self.stack[self.stack_index] > 128:
			self.stack[self.stack_index] -= 256
		#print(self.stack)
	def sub(self):
		
		self.stack[self.stack_index] -= 1
		if self.stack[self.stack_index] < -128:
			self.stack[self.stack_index] += 256
		#print(self.stack)	
	def right(self, x = 0):
		if len(self.stack)-1 > self.stack_index:
			self.stack_index += 1
		else:
			self.stack.append(x)
			self.stack_index += 1
	
	def input(self):
		temp = input()
		if len(temp) > 0:
			self.stack[self.stack_index] = ord(temp[0])
		else:
			self.stack[self.stack_index] = 0
	
	def open_file(self):
		#print("start")
		filename = ""
		tempfile = None
		outputstr = ""
		i = self.stack_index
		for x in range(self.stack[self.stack_index]):
			
			filename += chr(self.stack[self.stack_index+x+1])
		
		
		try:
			tempfile = open(filename, "r")
		except (OSError, IOError) as e:
			pass
		#print("got here")
		outputstr = tempfile.read()
		for x in range(len(outputstr)+1):
			self.right(ord(outputstr[x-1]))
		self.stack_index = i
		
	def append_code(self):
		
		temp = ""
		for x in range(self.stack[self.stack_index]):
			
			temp += chr(self.stack[self.stack_index+x+1])
		if len(temp) > 0:
			self.commands = self.commands + [y for y in temp]
			#print(self.commands)
	
	
	def left(self):
		if self.stack_index > 0:
			self.stack_index -= 1
		else:
			self.stack.insert(0, 0)
			self.stack_index = 0
	
	def output(self):
		#print(self.stack)
		sys.stdout.write(chr(self.stack[self.stack_index]))
	
	def loop(self):
		self.loop_start.append(self.index-1)
	
	
	
	def if_stmnt(self):
		if self.stack[self.stack_index] != 0:
			return True
		else:
			return False
	
	def loop_end(self):
		
		if self.if_stmnt():
			self.index = self.loop_start[-1]
		else:
			self.loop_start[:-1]
		
	
	
	def run(self, filename):
	
		self.file = open(filename, "r")
		code = self.file.read()
		
		self.commands = [x for x in code]
		
		while True:
			self.index = self.index + 1
			if self.index == len(self.commands):
				break
			
			if self.commands[self.index] in self.functions:
				#print(self.commands[self.index])
				#print(self.stack)
				self.functions[self.commands[self.index]]()
			
			
			
			
			
if __name__ == "__main__":
	cubd = Cubed()
	cubd.run(sys.argv[1])
		