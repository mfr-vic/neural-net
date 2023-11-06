import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import pygame
import random
from defs import *
from neuralNet import NeuralNet
from plataform import Plataform
from ballGenerator import BallGenerator
from plataformCollection import PlataformCollection

def update_label(data, title, font, x, y, gameDisplay):
		label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
		gameDisplay.blit(label, (x, y))
		return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, points, alive, max_points, font):
		y_pos = 10
		gap = 20
		x_pos = 10
		y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
		y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
		y_pos = update_label(num_iterations,'Iteração: ', font, x_pos, y_pos + gap, gameDisplay)
		y_pos = update_label(alive,'Total vivo', font, x_pos, y_pos + gap, gameDisplay)
		y_pos = update_label(points,'Pontuação atual:', font, x_pos, y_pos + gap, gameDisplay)
		y_pos = update_label(max_points,'Maior Pontuação:', font, x_pos, y_pos + gap, gameDisplay)

def run_game():
	pygame.init()
	gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display .set_caption("Cath the ball")

	clock = pygame.time.Clock()
	label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)
	
	running = True
	game_time= 0
	ballGenerator = BallGenerator(gameDisplay)
	plataformCollection = PlataformCollection(gameDisplay, ballGenerator)
	max_points = 0

	while running:
		dt = clock.tick(30)
		if(dt > 120):
			dt = 120
		game_time += dt

		gameDisplay.fill((0,0,0))

		plataformCollection.update(dt)
		points = plataformCollection.gex_max_points()
		alive = plataformCollection.get_alive()
		generation = plataformCollection.get_generation()

		if(points > max_points):
			max_points = points

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		update_data_labels(gameDisplay, dt, game_time, generation, points, alive, max_points, label_font)
		pygame.display.update()

if __name__ == "__main__":
	run_game()