import pygame, os, sys, random
import pygame.font
import numpy as np
from time import gmtime, strftime
from constants import *
from population_manager import PopulatioManager

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


def main(bird_list = None):
	population_manager = PopulatioManager(POPULATION_SIZE,
							 MUTATIONS_PER_GENOME, 
							 MUTATION_PROBABILITY, 
							 SCREEN)
	
	clock = pygame.time.Clock()
	run = True
	base_list = [Base(0), Base(BASE_WIDTH), Base(2*BASE_WIDTH)]
	pipe_list = [Pipe(WIDTH,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+PIPE_WIDTH+PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+2*PIPE_WIDTH+2*PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND))]
	
	if not bird_list:
		bird_list = population_manager.generate_population()

	time_for_decision = 10 # frame
	
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
		draw_base(base_list)
		draw_pipes(pipe_list)
		time_for_decision -= 1

		# bird_list updates
		for bird in bird_list:
			if bird.is_alive:
				# score
				if pipe_list[0].x + PIPE_WIDTH/2 == bird.x:
						bird.score += 1

				# dead or alive
				if not check_for_collisions(bird, pipe_list, base_list):
					bird.is_alive = False

				# features for bird
				x0 = bird.x - pipe_list[0].x # forward
				x1 = bird.y - (pipe_list[0].y - PIPE_GAP) # upward 
				x2 = bird.y - pipe_list[0].y # downward
				X = np.array([x0,x1,x2])

				# decision to jump
				if time_for_decision == 0:
					decision = bird.brain.decision(X)
					if decision >= 0.5:
						bird.jump()
						time_for_decision = 1

				# draw, and update pos
				bird.draw()
				bird.current_sprite += bird.sprite_incrementation
				if int(bird.current_sprite) >= 3:
					bird.current_sprite = 0
				bird.update_location()


		alive_birds_count= get_alive_birds_count(bird_list)
		# print(f"Alive birds: {alive_birds_count}")

		if alive_birds_count < 1:
			# bird_list = reproduce(bird_list) # new population
			for bird in bird_list:
				bird.is_alive = True
				bird.x = BIRD_X_INIT
				bird.y = BIRD_Y_INIT
				bird.y_vel = 0

			bird_list = bird_list
			bird_list = population_manager.generate_population()
			main(bird_list=bird_list)

		pygame.display.update()

def get_alive_birds_count(bird_list):
	count = 0
	for bird in bird_list:
		if bird.is_alive:
			count += 1
	return count

#BASE
class Base():
	def __init__(self, x = 0, y=HEIGHT-50):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, BASE_WIDTH, BASE_HEIGHT)


	def move(self):
		self.x -= BASE_SPEED
		self.rect.x = self.x

	def draw(self):
		SCREEN.blit(BASE_IMAGE,(self.x, self.y))

def draw_base(base_list):
	for i in range(len(base_list)-1,-1,-1):
		base = base_list[i] 
		base.move()
		base.draw()
		if i == 0 and base.x+BASE_WIDTH < -50:
			base.x = base_list[-1].x+BASE_WIDTH-1
			base_list.append(Base(base.x))
			base_list.pop(0)

#PIPE, contains both the top and bottom pipes
class Pipe():

	def __init__(self, x, y): # y is for bottom pipe
		self.x = x
		self.y = y
		self.rects = [pygame.Rect(self.x, self.y, PIPE_WIDTH, PIPE_HEIGHT), 
						pygame.Rect(self.x, self.y-PIPE_GAP-PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)] #bottom, top

	def draw(self):
		SCREEN.blit(PIPE_IMAGE, (self.x, self.y)) #bottom
		SCREEN.blit(pygame.transform.rotate(PIPE_IMAGE,180),(self.x, self.y-PIPE_GAP-PIPE_HEIGHT)) #top
		#pygame.draw.rect(SCREEN, (0,0,0), self.rects[0])
		#pygame.draw.rect(SCREEN, (0,0,0), self.rects[1])

	def move(self):
		self.x -= BASE_SPEED 
		for rect in self.rects:
			rect.x = self.x 
		 
def draw_pipes(pipe_list):
	for i in range(len(pipe_list)-1,-1,-1):
		pipe = pipe_list[i]
		pipe.move()
		pipe.draw()
		if i == 0 and pipe.x+PIPE_WIDTH < -50:
			pipe.x = pipe_list[-1].x + PIPE_WIDTH +PIPE_DISTANCE
			pipe_list.append(Pipe(pipe.x, random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)))
			pipe_list.pop(0)
			
def check_for_collisions(bird, pipe_list, base_list):
	length = len(pipe_list)
	for i in range(length):
		if bird.rect.colliderect(pipe_list[i].rects[0]) or bird.rect.colliderect(pipe_list[i].rects[1]):
			return False 
		if bird.rect.colliderect(base_list[i].rect) or bird.rect.colliderect(base_list[i].rect) or bird.rect.colliderect(base_list[i].rect):
			return False 
	return True

def draw_score(score):
	text = str(score)
	text_img = SCORE_FONT.render(text, True, (0,0,0))
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2,100+5))
	text_img = SCORE_FONT.render(text, True, (255,255,255))
	SCREEN.blit(text_img, (WIDTH//2-text_img.get_width()//2,100))
	
if __name__ == '__main__':
	main()

