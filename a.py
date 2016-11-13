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
USE_SDL = False
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

def printScreen5(screen):
	f = open("background3.txt","w")
	for i in xrange(210):
		string = ""
		prev = -1
		for j in xrange(160):
			pos = i*160+ j
			k = screen[pos]
			if k!= 144 and k != 74 and k != 0:
				string += str(k) + ","
				prev = k
			else:
				if k == 144:
					string += ";"
				if k == 74:
					string += "|"
		f.write(string + "\n")
	f.close()

def printScreen3(screen):
	f = open("background4.txt","w")
	for i in xrange(210):
		string = ""
		prev = -1
		for j in xrange(160):
			pos = i*160+ j
			k = screen[pos]
			if k!= 144 and k != 74 and k != 0 and k != 24 and k != 68 and k != 40:
				string += ";"
				prev = k
			else:
				if k == 24 or k == 68 or k == 40 or k == 0:
					string += "*"
				if k == 144:
					string += ";"
				if k == 74:
					v1 = False
					v2 = False
					v3 = False
					v4 = False
					if j < 157:
						v1 = screen[pos+1] == 74 and screen[pos+2] == 74 and screen[pos +3] == 74 
					if j < 158 and j > 0:
						v2 = screen[pos - 1] == 74 and screen[pos +1] == 74 and screen[pos+2] == 74
					if j < 159 and j > 1:
						v3 = screen[pos- 1] == 74 and screen[pos +1] == 74 and screen[pos -2] == 74
					if j > 2:
						v4 = screen[pos - 1] == 74 and screen[pos - 3] == 74 and screen[pos -2] == 74
					v5 = False
					v6 = False
					if i > 1 :
						v5 = screen[160*(i-2) + j] == 74
					if i < 208 :
						v6 = screen[160*(i+2) + j] == 74 
					if (((not v1)and(not v2) and (not v3) and v4) or ((not v1)and(not v2) and (not v4) and v3) or ((not v1)and(not v4) and (not v3) and v2) or ((not v4)and(not v2) and (not v3) and v1))  and (not v5) and (not v6):
						string += ";"
					else:
						string += "|"
						
						
		f.write("l:" + str(i) + string + "\n")
	f.close()

def printScreen4(screen):
	bg = get_background("background4.txt")
	f = open("object2.txt","w")
	for i in xrange(210):
		string = ""
		prev = -1
		for j in xrange(160):
			pos = i*160+ j
			k = screen[pos]
			if k == bg[pos]:
				string += "."
				prev = k
			else:
				if k == 144:
					string += ";"
				elif k == 74:
					string += "|"
				elif k == 42 or  k == 89:
					string += "!"
				else:
					string += str(k) +","
		f.write(string + "\n")
	f.close()
	 
def get_background(file_name):
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
		

for episode in xrange(200):
	total_reward = 0
	k = 0
	while not ale.game_over():
		a = legal_actions[randrange(len(legal_actions))]
		# Apply an action and get the resulting reward
		reward = ale.act(a);
		if reward > 10:
			print "happened"
			screen = ale.getScreen()
			printScreen4(screen)
		total_reward += reward
	print 'Episode', episode, 'ended with score:', total_reward
	ale.reset_game()
 

