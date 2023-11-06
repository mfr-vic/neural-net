import pygame
import random
from defs import *
import numpy as np

class Plataform():
	def __init__(self, gameDisplay, brain):
		self.gameDisplay = gameDisplay;
		self.x = PLATAFORM_POSITION[0]
		self.y = PLATAFORM_POSITION[1]
		self.plat_color = self.random_color()
		self.rect = self.draw()
		self.points = 0
		self.brain = brain
		self.fitness = 0
		self.is_alive = True
		self.last_catched_ball = None

	def move_left(self):
		speed = PLATAFORM_SPEED
		if(self.x - speed < 0):
			self.x = 0
		else:
			self.x = self.x - speed

	def move_right(self):
		speed = PLATAFORM_SPEED
		if(self.x + speed > WINDOW_WIDTH - PLATAFORM[0]):
			self.x = WINDOW_WIDTH -  PLATAFORM[0]
		else:
			self.x = self.x + speed

	def draw(self):
		self.rect = pygame.draw.rect(
			self.gameDisplay, 
			self.plat_color, 
			pygame.Rect(self.x, self.y, PLATAFORM[0], PLATAFORM[1]))

		return self.rect

	def random_color(self):
		rgbl=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		return tuple(rgbl)


	def update(self):
		if(self.lost_game() == False):
			self.draw()

	def lost_game(self):
		return self.is_alive == False;
	
	def kill(self):
		self.is_alive = False

	def reset(self):
		self.is_alive = True
		self.last_catched_ball = None
		self.points = 0
		self.fitness = 0

	def get_points(self):
		return self.points

	def get_rect(self):
		return self.rect

	def try_to_catch(self, ball):
		if(self.last_catched_ball == ball):
			return
		if(self._catched_the_ball(ball)):
			self.last_catched_ball = ball
			self.points += 1
			return
		self.set_fitness(ball)
		self.kill()

	def set_fitness(self, ball):
		ball_points = self.points * WINDOW_WIDTH
		if(ball.center_x > self.x):
			self.fitness = ball_points + (WINDOW_WIDTH - (ball.center_x - self.x))
		else:
			self.fitness = ball_points + (WINDOW_WIDTH - (self.x - ball.center_x))

	def _catched_the_ball(self, ball):
		return pygame.Rect(self.x, self.y, PLATAFORM[0], PLATAFORM[1]).colliderect(ball.get_rect())

	def predict(self, ballGenerator):
		ball = ballGenerator.ball
		input = np.array([[(self.x + PLATAFORM[0] / 2) - ball.center_x],[ ball.center_y]])

		left, right = self.brain.predict(input)
		if(left > right):
			self.move_left()
		else:
			self.move_right()