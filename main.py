import pygame, os, sys, random
import pygame.font
import numpy as np
from time import gmtime, strftime
from constants import *
from game_util import *
from population_manager import PopulatioManager


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


def main(population_manager = None):
	if not population_manager:
		population_manager = PopulatioManager(SCREEN)
	
	clock = pygame.time.Clock()
	run = True
	base_list = [Base(0), Base(BASE_WIDTH), Base(2*BASE_WIDTH)]
	pipe_list = [Pipe(WIDTH,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+PIPE_WIDTH+PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+2*PIPE_WIDTH+2*PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND))]
	
	while run:
		clock.tick(75)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
					sys.exit()

		SCREEN.blit(BACKGROUND_IMAGE,(0,0))
		draw_base(base_list, SCREEN)
		draw_pipes(pipe_list, SCREEN)

		population_manager.time_for_decision -= 1

		alive_birds_count= population_manager.get_alive_birds_count()
		print(f"Alive birds: {alive_birds_count}")

		if alive_birds_count < 1:
			#population_manager.generate_population()
			population_manager.survival_of_the_fittest()
			# main(population_manager)

		else:
			population_manager.update_population(pipe_list, base_list)

		pygame.display.update()




if __name__ == '__main__':
	main()

