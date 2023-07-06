import pygame, os, sys, random
import pygame.font
import numpy as np
from time import gmtime, strftime
from constants import *

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


def main(player_playing = True, is_training = False):
	clock = pygame.time.Clock()
	run = True
	start = False if player_playing else True
	score = 0 
	base_list = [Base(0), Base(BASE_WIDTH), Base(2*BASE_WIDTH)]
	pipe_list = [Pipe(WIDTH,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+PIPE_WIDTH+PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+2*PIPE_WIDTH+2*PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND))]
	bird = Bird()

	time_for_decision = 0

	if is_training:
		training_data = []

	while run:
		clock.tick(75)
		jumped_this_frame = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
					sys.exit()
				elif event.key == pygame.K_SPACE and player_playing:
					start = True
					bird.jump()	

		if start and is_training:
			y = 1 if jumped_this_frame else 0
			p0 = pipe_list[0]
			p1 = pipe_list[1]
			x = [bird.y, p0.x, p0.y, p0.y-PIPE_GAP-PIPE_HEIGHT, 
				 p1.x, p1.y, p1.y-PIPE_GAP-PIPE_HEIGHT]
			training_data.append((x, y))
			# print(training_data)

		if not player_playing and time_for_decision<=0:
			value = random.randint(0,10)/10
			print(value)
			if value > 0.7 and time_for_decision<=0:
				start = True
				bird.jump()
				time_for_decision += 40
			time_for_decision -= 1

		SCREEN.blit(BACKGROUND_IMAGE,(0,0))

		draw_base(base_list)
		bird.draw()
		bird.current_sprite += bird.sprite_incrementation
		if int(bird.current_sprite) >= 3:
			bird.current_sprite = 0

		if start:
			bird.update_location()
			draw_pipes(pipe_list)

		#score update
		#print(pipe_list[0].x + PIPE_WIDTH, bird.x)
		if pipe_list[0].x + PIPE_WIDTH/2 == bird.x:
			score += 1
			print("Score: ",score)
		draw_score(score)

		if not check_for_collisions(bird, pipe_list, base_list):
			run = False
			if score > 10:
				print("saving the training data")
				filename = strftime("%Y-%m-%d %H-%M-%S", gmtime())
				np.save(f"training_data/{filename}", training_data)
			print("Restarting Game")
			pygame.time.delay(1000)
			main(player_playing, is_training)

		pygame.display.update()

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
			
#BIRD
class Bird():
	def __init__(self):
		self.x = 200
		self.y = 400
		self.sprite = BIRD_SPRITE
		self.current_sprite = 0
		self.y_vel = 0
		self.acceleration_y = 9.8
		self.time_passed = 0.03 #since the last loop
		self.sprite_incrementation = 0.1
		self.create_rect()

	def jump(self):
		self.y_vel = -7

	def update_location(self): #accelerate, move, update_sprite
		self.y_vel += self.acceleration_y*self.time_passed

		
		self.move()
		self.create_rect()


	def move(self):
		self.y += self.y_vel
	def create_rect(self):
		self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)
	def draw(self):
		SCREEN.blit(self.sprite[int(self.current_sprite)], (self.x, self.y))

def check_for_collisions(bird, pipe_list, base_list):
	length = len(pipe_list)
	for i in range(length):
		if bird.rect.colliderect(pipe_list[i].rects[0]) or bird.rect.colliderect(pipe_list[i].rects[1]):
			print("Gameover") 
			return False 
		if bird.rect.colliderect(base_list[i].rect) or bird.rect.colliderect(base_list[i].rect) or bird.rect.colliderect(base_list[i].rect):
			print("Gameover")
			return False 
	return True

def draw_score(score):
	text = str(score)
	text_img = SCORE_FONT.render(text, True, (0,0,0))
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2,100+5))
	text_img = SCORE_FONT.render(text, True, (255,255,255))
	SCREEN.blit(text_img, (WIDTH//2-text_img.get_width()//2,100))
	

if __name__ == '__main__':
	main(True, True)

