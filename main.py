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
		population_manager.update_population(pipe_list, base_list)

		# bird_list updates
		# for bird in population_manager.population:
		# 	if bird.is_alive:
		# 		# score
		# 		if pipe_list[0].x + PIPE_WIDTH/2 == bird.x:
		# 				bird.score += 1

		# 		# dead or alive
		# 		if not check_for_collisions(bird, pipe_list, base_list):
		# 			bird.is_alive = False

		# 		# features for bird
		# 		x0 = bird.x - pipe_list[0].x # forward
		# 		x1 = bird.y - (pipe_list[0].y - PIPE_GAP) # upward 
		# 		x2 = bird.y - pipe_list[0].y # downward
		# 		X = np.array([x0,x1,x2])

		# 		# decision to jump
		# 		if time_for_decision == 0:
		# 			decision = bird.brain.decision(X)
		# 			if decision >= 0.5:
		# 				bird.jump()
		# 				time_for_decision = 1

		# 		# draw, and update pos
		# 		bird.draw()
		# 		bird.current_sprite += bird.sprite_incrementation
		# 		if int(bird.current_sprite) >= 3:
		# 			bird.current_sprite = 0
		# 		bird.update_location()


		alive_birds_count= get_alive_birds_count(population_manager.population)
		print(f"Alive birds: {alive_birds_count}")

		if alive_birds_count < 1:
			# bird_list = reproduce(bird_list) # new population
			population_manager.generate_population()
			main(population_manager)

		pygame.display.update()

def get_alive_birds_count(bird_list):
	count = 0
	for bird in bird_list:
		if bird.is_alive:
			count += 1
	return count


if __name__ == '__main__':
	main()

