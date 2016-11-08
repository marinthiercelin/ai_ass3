import sys
from random import randrange
from ale_python_interface import ALEInterface
from screen import get_feature

class agent(object):
	def __init__(self):
		self.ale = ALEInterface()
		
		# Get & Set the desired settings
		self.ale.setInt('random_seed', 123)

		# Set USE_SDL to true to display the screen. ALE must be compilied
		# with SDL enabled for this to work. On OSX, pygame init is used to
		# proxy-call SDL_main.
		USE_SDL = False
		if USE_SDL:
		  if sys.platform == 'darwin':
			import pygame
			pygame.init()
			self.ale.setBool('sound', False) # Sound doesn't work on OSX
		  elif sys.platform.startswith('linux'):
			self.ale.setBool('sound', True)
		  self.ale.setBool('display_screen', True)

		# Load the ROM file
		self.ale.loadROM("ms_pacman.bin")
		#persistent:
		self.tetas = []
		self.Q = self.txtToMap('qvalues.txt') #, a table of action values indexedby state and action, initially zero
		self.N = self.txtToMap('nvalues.txt') #, a table of frequenciesfor state-action pairs, initially zero
		self.s = None
		self.a = None
		self.r = 0
		self.actions = self.ale.getMinimalActionSet()
		print self.actions
		#the previous state, action, and reward, initially null

	def Q_LEARNING_AGENT(self,state,reward):
		if self.ale.game_over():
			self.updateQ(self.s,None,reward)
		if self.s is not None: 
			self.incrementN(self.s,self.a) 
			val = self.computeNewQ(self.s,self.a,self.r,state)
			self.updateQ(self.s,self.a,val) 
		self.s = state
		self.a = self.chooseAct(state)
		self.r = reward 
		return self.a
			
	def computeNewQ(self, s,a,reward,state):
		qsa = self.getQ(s,a)
		maxQ = self.getQ(state,self.actions[0])
		for act in self.actions:
			val = self.getQ(state,act)
			if val > maxQ: 
				maxQ = val
		n = self.getN(s,a)
		alp = self.alpha(n)
		v = qsa  + alp*(reward + 0.9*maxQ - qsa)
		return v

	def chooseAct(self,state):
		v = randrange(10)
		if v == 5: return self.actions[randrange(len(self.actions))]
		a = self.actions[0]
		maxQ = self.getQ(state,self.actions[0])
		for act in self.actions:
			val = self.getQ(state,act)
			if val > maxQ: 
				maxQ = val
				a = act
		return a
			
		
	def alpha(self,Nsa):
		return 0.9
		

	def updateQ(self,s,a, value):
		self.Q[str(s)+"/"+str(a)] = value
	def getQ(self,s,a):
		return self.Q.get(str(s)+"/" +str(a), 0)
	def incrementN(self,s,a):
		self.N[str(s)+"/" +str(a)] = self.getN(s,a) + 1
	def getN(self,s,a):
		return  self.N.get(str(s)+"/"+str(a), 0)
		
	def play(self, number):
		for episode in xrange(number):
			total_reward = 0
			self.s = None
			self.a = None
			reward = 0
			while not self.ale.game_over():
				state = hash(get_feature(self.ale.getScreen()))
				action = self.Q_LEARNING_AGENT(state,reward)
				# Apply an action and get the resulting reward
				reward =self.ale.act(action);
				total_reward += reward
			print 'Episode', episode, 'ended with score:', total_reward
			self.ale.reset_game()
		self.mapToTxt(self.Q, 'qvalues.txt')
		self.mapToTxt(self.N, 'nvalues.txt')
			
	def mapToTxt(self, hMap, filepath):
		f = open(filepath, 'r+')
		for elem in hMap.keys():
			toWrite = str(elem) + " " + str(hMap[elem]) + "\n"
			f.write(toWrite)
		f.close(); 

		
	def txtToMap(self, filepath): 
		newMap = {}
		f = open(filepath)
		while True:
			string = f.readline(); 
			if not string: break
			tmp = self.stringSplitter(string)
			newMap[tmp[0]] = float(tmp[1]); 
		f.close()
		return newMap; 

	def stringSplitter(self, string): 
		i = string.find(' '); 
		head = string[:i]
		rest = string[i+1: len(string)-1] # getting rid of the \n's
		return (head, rest)
		
player = agent()
player.play(2)
