class tracker(object):
	def __init__(self, ale):
		self.ale = ale
		self.x = 0
		self.y = 0
		self. pacpos = (-1,-1)
		self.background = self.get_background("background4.txt")
	
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
		return col not in [42, 144, 0, 74, 89, 84, 58, 68, 24, 148] # All those are nice colors
	
	def findPac(self,sub):
		pacpos = (-1,-1)
		(i,j) = self.pacpos
		if self.pacpos != (-1,-1):
			if 89 in sub[i*10+j] or 42 in sub[i*10+j]: return (i,j)
			if (i<12) and (89 in sub[(i+1)*10+j] or 42 in sub[(i+1)*10+j]):
				self.pacpos =(i+1,j)
			if (i > 0) and ( 89 in sub[(i-1)*10+j] or 42 in sub[(i-1)*10+j]):
				self.pacpos =(i-1,j) 
				return (i-1,j)
			if (j < 9) and (89 in sub[i*10+j+1] or 42 in sub[i*10+j+1]):
				self.pacpos =(i,j+1) 
				return (i,j+1)
			if (j > 0) and (89 in sub[i*10+j-1] or 42 in sub[i*10+j-1]):
				self.pacpos =(i,j-1) 
				return (i,j-1)
				
		for k in xrange(13):
			for l in xrange(10):
				if 89 in sub[k*10+l] or 42 in sub[k*10+l]:
					pacpos = (k,l)
					break
			if pacpos != (-1,-1) : break
		self.pacpos = pacpos
		return pacpos
		
	def getState(self):
		res = self.divideScreen(self.ale.getScreen())
		if res[1] == False:
			return (-2,-2,-2,-2,-2,-2,-2,-2)#no ghosts weird state
		sub = res[0]
		pacpos = self.findPac(sub)
		ND, NP, NB , WD, WP, WB, ED, EP, EB, SD ,SP, SB = -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1
		
		if pacpos == (-1,-1) : return (-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2)
		
		k = pacpos[0]
		l = pacpos[1]
		if k > 0 :
			ND , NP, NB = 0,0,0
			if self.cont_Danger(sub[(k-1)*10 + l]) :
				ND = 1
			if 74 in sub[(k-1)*10 + l]:
				NP = 1
			if 148 in sub[(k-1)*10 + l]:
				NB = 1
			if k > 1 :
				if self.cont_Danger(sub[(k-2)*10 + l]) :
					ND = 1
				if 74 in sub[(k-2)*10 + l]:
					NP = 1
				if 148 in sub[(k-2)*10 + l]:
					NB = 1
		
		if k < 12 :
			SD , SP, SB = 0,0,0
			if self.cont_Danger(sub[(k+1)*10 + l]) :
				SD = 1
			if 74 in sub[(k+1)*10 + l]:
				SP = 1
			if 148 in sub[(k+1)*10 + l]:
				SB = 1
			if k < 11 :
				if self.cont_Danger(sub[(k+2)*10 + l]) :
					SD = 1
				if 74 in sub[(k+2)*10 + l]:
					SP = 1
				if 148 in sub[(k+2)*10 + l]:
					SB = 1
				
		if l > 0 :
			WD , WP,WB = 0,0,0
			if self.cont_Danger(sub[(k)*10 + l -1]) :
				WD = 1
			if 74 in sub[(k)*10 + l -1]:
				WP = 1
			if 148 in sub[(k)*10 + l -1]:
				WB = 1
			if l > 1 :
				if self.cont_Danger(sub[(k)*10 + l -2]) :
					WD = 1
				if 74 in sub[(k)*10 + l -2]:
					WP = 1
				if 148 in sub[(k)*10 + l -2]:
					WB = 1
				
		if l < 9 :
			ED , EP, EB = 0,0,0
			if self.cont_Danger(sub[(k)*10 + l+1]) :
				ED = 1
			if 74 in sub[(k)*10 + l +1]:
				EP = 1
			if 148 in sub[(k)*10 + l +1]:
				EB = 1
			if l < 8 :
				if self.cont_Danger(sub[(k)*10 + l +2]) :
					ED = 1
				if 74 in sub[(k)*10 + l +2]:
					EP = 1
				if 148 in sub[(k)*10 + l +2]:
					EB = 1
				
		return (ND,NP,NB,WD,WP,WB,ED,EP,EB,SD,SP,SB)
		
			
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
	
	def divideScreen(self,screen):
		boo = False
		features = 13*10*[[]]
		string = ""
		for i in range(169):
			for j in range(160):
				pos = 160*(i+1) + j 
				color = screen[pos]
				if color != self.background[pos]:
					if color != 89 and  color != 42 and  color != 74 and  color != 0:
						boo = True
					k = (i - (i%13))/13
					l = (j - (j%16))/16
					cop = features[k*10 + l][:]
					cop.append(color)
					features[k*10 + l] = cop
		return (features,boo)
			
		
		
