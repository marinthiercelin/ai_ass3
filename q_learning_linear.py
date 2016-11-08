import sys
from random import randrange
from ale_python_interface import ALEInterface
from screen_linear import get_feature

#q_learning with linear function approximation
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
		self.weights = 16*14*128*4*[0] # one weight for every pair of (color action) in every sub_screen
		self.N = {} #, a table of frequenciesfor state-action pairs, initially zero
		self.actions = [2,3,4,5]
		self.discount = 0.99
		self.alpha = 0.9
		print self.actions
		#the previous state, action, and reward, initially null

	def Q_LEARNING_AGENT(self,state,reward):
		#if self.ale.game_over():
			#self.updateQ(self.last_state,None,self.last_reward)
		if self.last_state is not None: 
			self.incrementN(self.last_state,self.last_action) 
			q_diff = self.computeQDiff(self.last_state,self.last_action,self.last_reward,state)
			self.update_weights(self.last_state,self.last_action,q_diff) 
		self.last_state = state
		self.last_action = self.chooseAct(state)
		self.last_reward = reward 
		return self.last_action
	
	def update_weights(self,state, action, q_diff):
		state_tab = state[0]
		for sub_screen in xrange(len(state_tab)):
			for color in state_tab[sub_screen]:
				val = self.getWeight(sub_screen,color,action) + self.get_alpha(state,action)*q_diff
				self.updateWeight(sub_screen,color,action,val)
			
	def computeQDiff(self, s,a,reward,state):
		qsa = self.getQ(s,a)
		maxQ = self.get_max_action(state)[1]
		v = (reward + self.discount*maxQ - qsa)
		return v

	def chooseAct(self,state):
		v = randrange(10)
		if v == 5: return self.actions[randrange(len(self.actions))]
		return self.get_max_action(state)[0]
		
	def get_max_action(self,state):
		a = self.actions[0]
		maxQ = self.getQ(state,self.actions[0])
		for act in self.actions:
			val = self.getQ(state,act)
			if val > maxQ: 
				maxQ = val
				a = act
		return (a,maxQ)
			
		
	def get_alpha(self,state,action):
		return self.alpha
		
	def getWeight(self,sub_screen,color,action):
		index = sub_screen*4*128 + color*4 + action
		return self.weights[index]
	
	def updateWeight(self,sub_screen,color,action,value):
		index = sub_screen*4*128 + color*4 + action
		self.weights[index] = value
		
	def getQ(self,state,action):
		state_tab = state[0]
		q = 0
		for sub_screen in xrange(len(state_tab)):
			for color in state_tab[sub_screen]:
				q += self.getWeight(sub_screen,color,action)
		return q
		
	def incrementN(self,state,action):
		self.N[str(state[1]) + "/" +str(action)] = self.getN(state,action) + 1
	
	def getN(self,s,a):
		return  self.N.get(str(s)+"/"+str(a), 0)
		
	def play(self, number):
		for episode in xrange(number):
			total_reward = self.one_game()
			print 'Episode', episode, 'ended with score:', total_reward
			self.ale.reset_game()
	
	def one_game(self):
		total_reward = 0
		self.last_state = get_feature(self.ale.getScreen())
		self.last_action = self.chooseAct(self.last_state)
		self.last_reward = self.ale.act(self.last_action)
		curr_reward = 0
		life = self.ale.lives()
		print life
		while not self.ale.game_over():
			curr_state = get_feature(self.ale.getScreen())
			action = self.Q_LEARNING_AGENT(curr_state,curr_reward)
			# Apply an action and get the resulting reward
			curr_reward = self.ale.act(action)
			if life > self.ale.lives():
				curr_reward = -100
				life = self.ale.lives()
				print life
			total_reward += curr_reward
		return total_reward
		
	def mapToTxt(self, hMap, filepath):
		f = open(filepath, 'r+')
		for elem in hMap.keys():
			toWrite = str(elem) + " " + str(hMap[elem]) + "\n"
			f.write(toWrite)
		f.close(); 
		
	def listToTxt(self, w_list, filepath):
		f = open(filepath, 'w')
		for elem in w_list:
			toWrite = str(elem)+"\n"
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
	
	def txtToList(self, filepath): 
		w_list = []
		f = open(filepath)
		for string in f:
			w_list.append(float(string))
		f.close()
		return w_list; 

	def stringSplitter(self, string): 
		i = string.find(' '); 
		head = string[:i]
		rest = string[i+1: len(string)-1] # getting rid of the \n's
		return (head, rest)
	
	def loadN(self,filename):
		self.N = self.txtToMap(filename)
	def loadW(self, filename):
		self.weights = self.txtToList(filename)
	def saveN(self,filename):
		self.mapToTxt(self.N,filename)
	def saveW(self,filename):
		self.listToTxt(self.weights,filename)
		
player = agent()
player.play(1)
player.saveN("n_map.txt")
player.saveW("w_list.txt")
