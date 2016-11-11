#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
from ale_python_interface import ALEInterface

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = True
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM("ms_pacman.bin")

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

def findZePac(x, y): 
	screen = ale.getScreen()
	for i in xrange(x-1, x+2):
		for j in xrange(y-1, y+2): 
			if screen[i*160 + j] == 42: 
				return (i, j)
	for i in xrange(x-3, x+4):
		for j in xrange(y-3, y+4): 
			if screen[i*160 + j] == 42: 
				#print " slightly better -- found : " + str((i, j)) + " prev : " + str((x, y))
				return (i, j)			
	for i in xrange(210):
		for j in xrange(160): 
			if screen[i*160 + j] == 42: 
				#print " why are you so noob ? " + str((x, y))
				return (i, j)
				
	return (0, 0)
	
def pacDanger(x, y):
	if x == 0 or y == 0: 
		return (1000, None)
	screen = ale.getScreen()
	dangers = []
	for i in xrange(x-30, x+31): 
		for j in xrange(y-30, y+31): 
			if isDanger(screen[i*160 + j]):
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
				  

def isDanger(col): 
	return col not in [42, 144, 0, 74, 89, 68, 24] # All those are nice colors 

prevpos = (0, 0)
pacpos = (0, 0)

# Play 10 episodes
for episode in xrange(10):
	total_reward = 0
	while not ale.game_over():
		prevpos = pacpos
		pacpos = findZePac(prevpos[0], prevpos[1])
		print pacDanger(pacpos[0], pacpos[1]) 
	
		a = legal_actions[randrange(len(legal_actions))]
		# Apply an action and get the resulting reward
		reward = ale.act(a);
		total_reward += reward
	print 'Episode', episode, 'ended with score:', total_reward
	ale.reset_game()


