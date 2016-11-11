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
ale.loadROM('ms_pacman.bin')

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()
# Play 10 episodes

def printScreen(screen):
	for i in xrange(210):
		string = ""
		prev = -1
		for j in xrange(160):
			k = screen[i*160+ j]
			if k != prev and k!= 144 and k != 74 and k != 0:
				string += "c: " +str(j) + " " + str(k) + " "
				prev = k
		print string + " l: " +str(i)

def printScreen2(screen):
	for i in xrange(210):
		string = ""
		prev = -1
		for j in xrange(160):
			k = screen[i*160+ j]
			if k!= 144 and k != 74 and k != 0:
				string += str(k) + ","
				prev = k
			else:
				string += "-"
		print " l: " +str(i)+string 

for episode in xrange(1):
	total_reward = 0
	k = 0
	while not ale.game_over():
		if k == 600:
			screen = ale.getScreen()
			#printScreen(screen)
			printScreen2(screen)
		k += 1
		a = legal_actions[randrange(len(legal_actions))]
		# Apply an action and get the resulting reward
		reward = ale.act(a);
		total_reward += reward
	print 'Episode', episode, 'ended with score:', total_reward
	ale.reset_game()
 

