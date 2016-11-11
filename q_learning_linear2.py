import sys
from random import randrange
from ale_python_interface import ALEInterface
from screen_linear import get_feature
from game import game
from screen_tracker import tracker
import q_io

#q_learning with linear function approximation
class agent(object):
	def __init__(self,display):
		self.ale = game(display)
		self.tracker = tracker(self.ale) 
		#persistent:
		#, a table of action values indexedby state and action, initially zero
		self.load('n_values.txt','q_values.txt') #, a table of frequenciesfor state-action pairs, initially zero 
		self.actions = [2,3,4,5]
		self.discount = 0.99
		self.alpha = 0.9
		#the previous state, action, and reward, initially null

	def Q_LEARNING_AGENT(self,state,reward):
		if self.last_state is not None: 
			self.incrementN(self.last_state,self.last_action) 
			new = self.computeNewQ(self.last_state,self.last_action,reward,state)
			self.updateQ(self.last_state, self.last_action, new) 
		self.last_state = state
		self.last_action = self.chooseAct(state)
		return self.last_action
	
			
	def computeNewQ(self, s,a,reward,state):
		qsa = self.getQ(s,a)
		maxQ = self.get_max_action(state)[1]
		#print "value of state 1 " + str(qsa) + " value of state 2 " + str(maxQ)
		v = (reward + self.discount*maxQ - qsa)
		#if abs(v) < 0.01:
		#	v = 0
		return qsa + self.get_alpha(s,a)*v 

	def chooseAct(self,state):
		v = randrange(10)
		if v == 5: return self.actions[randrange(len(self.actions))]
		return self.get_max_action(state)[0]
		
	def get_max_action(self,state):
		a = self.actions[0]
		maxQ = self.getQ(state,self.actions[0])
		for act in self.actions[1:]:
			val = self.getQ(state,act)
			if val > maxQ or (val == maxQ and randrange(10) == 5): 
				maxQ = val
				a = act
		return (a,maxQ)
			
		
	def get_alpha(self,state,action):
		return self.alpha
		
	
	def updateQ(self,s,a, value):
		self.Q[str(s)+"/"+str(a)] = value
	def getQ(self,s,a):
		return self.Q.get(str(s)+"/" +str(a), 0)
		
	def incrementN(self,state,action):
		self.N[str(state) + "/" +str(action)] = self.getN(state,action) + 1
	
	def getN(self,s,a):
		return  self.N.get(str(s)+"/"+str(a), 0)
		
	def play(self, number):
		summ = 0
		for episode in xrange(number):
			total_reward = self.one_game()
			summ += total_reward
			print 'Episode', episode, 'ended with score:', total_reward
			self.ale.reset_game()
			self.save('n_values.txt','q_values.txt')
		q_io.save_average('av.txt',number,summ*1.0/number)
	
	def one_game(self):
		total_reward = 0
		self.last_state = self.tracker.pacDanger()
		self.last_action = self.chooseAct(self.last_state)
		curr_reward = self.ale.act(self.last_action)
		life = self.ale.lives()
		print life
		while not self.ale.game_over():
			if curr_reward != 0:
				print curr_reward
			curr_state = self.tracker.pacDanger()
			action = self.Q_LEARNING_AGENT(curr_state,curr_reward)
			# Apply an action and get the resulting reward
			curr_reward = self.ale.act(action)
			if life > self.ale.lives():
				curr_reward = -100
				life = self.ale.lives()
				print life
			total_reward += curr_reward
		return total_reward + 300
		
	
	def load(self,filename_n, filename_q):
		self.N = q_io.txtToMap(filename_n)
		self.Q = q_io.txtToMap(filename_q)
	def save(self,filename_n, filename_q):
		q_io.mapToTxt(self.N,filename_n)
		q_io.mapToTxt(self.Q,filename_q)
		
player = agent(False)
player.play(50)
