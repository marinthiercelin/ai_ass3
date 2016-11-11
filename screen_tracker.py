class tracker(object):
	def __init__(self, ale):
		self.ale = ale
		self.x = 0
		self.y = 0
	
	def findZePac(self):
		x = self.x
		y = self.y 
		screen = self.ale.getScreen()
		for i in xrange(x-1, x+2):
			for j in xrange(y-1, y+2): 
				if screen[i*160 + j] == 42:
					self.x = i
					self.y = j 
					return (i, j)
		for i in xrange(x-3, x+4):
			for j in xrange(y-3, y+4): 
				if screen[i*160 + j] == 42: 
					#print " slightly better -- found : " + str((i, j)) + " prev : " + str((x, y))
					self.x = i
					self.y = j
					return (i, j)			
		for i in xrange(210):
			for j in xrange(160): 
				if screen[i*160 + j] == 42: 
					#print " why are you so noob ? " + str((x, y))
					self.x = i
					self.y = j
					return (i, j)
		self.x = 0
		self.y = 0			
		return (0, 0)
		
	def pacDanger(self):
		self.findZePac()
		x = self.x
		y = self.y
		if x == 0 or y == 0: 
			return (1000, None)
		screen = self.ale.getScreen()
		dangers = []
		for i in xrange(x-30, x+31): 
			for j in xrange(y-30, y+31): 
				if self.isDanger(screen[i*160 + j]):
					dist = abs(i-x) + abs(j-y)
					if abs(i-x) < abs(j-y): #Danger comes from West-East axis
						if j-y < 0 : 
							dangers.append((dist, "W"))
						else: 
							dangers.append((dist, "E"))
					else : #Danger comes from North-South axis
						if i-x < 0 : 
							dangers.append((dist, "N"))
						else:
							dangers.append((dist, "S"))
		closest = 1000
		priority = None 
		for i in xrange(len(dangers)):
			if dangers[i][0] < closest:
				priority = i
				closest = dangers[i][0]
		if priority != None: 
			return dangers[priority]
		else :
			return (1000, None)		
					  

	def isDanger(self,col): 
		return col not in [42, 144, 0, 74, 89, 68, 24] # All those are nice colors
