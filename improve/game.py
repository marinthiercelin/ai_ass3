import sys
from random import randrange
from ale_python_interface import ALEInterface

class game(object):
	def __init__(self,display):
		self.ale = ALEInterface()
		
		# Get & Set the desired settings
		self.ale.setInt('random_seed', 123)

		# Set USE_SDL to true to display the screen. ALE must be compilied
		# with SDL enabled for this to work. On OSX, pygame init is used to
		# proxy-call SDL_main.
		USE_SDL = display
		if USE_SDL:
		  if sys.platform == 'darwin':
			import pygame
			pygame.init()
			self.ale.setBool('sound', False) # Sound doesn't work on OSX
		  elif sys.platform.startswith('linux'):
			self.ale.setBool('sound', True)
		  self.ale.setBool('display_screen', True)

		# Load the ROM file
		self.ale.loadROM("../ms_pacman.bin")
	
	def act(self,action):
		return self.ale.act(action)
	
		
	def getScreen(self):
		return self.ale.getScreen()
		
	def reset_game(self):
		self.ale.reset_game()
	
	def lives(self):
		return self.ale.lives()
		
	def game_over(self):
		return self.ale.game_over()
	
