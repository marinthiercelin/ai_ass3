class tracker(object):
	def __init__(self, ale):
		self.ale = ale
		self.x = 0
		self.y = 0
		#self.background = self.get_background("background4.txt")
	
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
		return col not in [42, 144, 0, 74, 89, 84, 58, 68, 24] # All those are nice colors
	
	def computeState(self):
		sub = divide_screen(self.ale.getScreen())
		pacpos = (-1,-1)
		for k in xrange(13):
			for l in xrange(16):
				if 89 in sub[k*10+l] or 42 in sub[k*10+l]:
					pacpos = (k,l)
		ND, NP , WD, WP, ED, EP, SD ,SP = -1
		
		if pacpos == (-1,-1) : return (ND,NP,WD,WP,ED,EP,SD,SP)
		
		k = pos[0]
		l = pos[1]
		if k > 0 :
			ND , NP = 0
			if self.cont_Danger(sub[(k-1)*10 + l]) :
				ND = 1
			if 74 in sub[(k-1)*10 + l]:
				NP = 1
		
		if k < 12 :
			SD , SP = 0
			if self.cont_Danger(sub[(k+1)*10 + l]) :
				SD = 1
			if 74 in sub[(k+1)*10 + l]:
				SP = 1
		if l > 0 :
			WD , WP = 0
			if self.cont_Danger(sub[(k)*10 + l -1]) :
				WD = 1
			if 74 in sub[(k)*10 + l -1]:
				WP = 1
		if l < 9 :
			ED , EP = 0
			if self.cont_Danger(sub[(k)*10 + l +1]) :
				ED = 1
			if 74 in sub[(k)*10 + l +1]:
				EP = 1
		return (ND,NP,WD,WP,ED,EP,SD,SP)
		
			
	def cont_Danger(self, sub):
		for color in sub:
			if self.isDanger(color):
				return True
		return False
		
		
	def get_background(self,file_name):
		f = open(file_name,"r")
		bg = []
		while True:
			c = f.read(1)
			if not c:
				break
			if c == '*':
				bg.append(0)
			if c == ';':
				bg.append(144)
			if c == '|':
				bg.append(74)
		f.close()
		return bg
	
	def divideScreen(screen):
		features = 13*10*[[]]
		string = ""
		for i in range(169):
			for j in range(160):
				pos = 160*(i+1) + j 
				color = screen[pos]
				if color != self.background[pos]:
					k = (i - (i%13))/13
					l = (j - (j%16))/10
					features[k*10 + l].append(color) 
		return features
			
		
		
