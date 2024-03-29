from perceptron import Perceptron
from constants import *


#BIRD
class Bird():
	def __init__(self, screen, alpha = 1):
		self.screen = screen
		self.alpha = alpha
		self.x = BIRD_X_INIT
		self.y = BIRD_Y_INIT
		self.sprite = BIRD_SPRITE
		self.current_sprite = 0
		self.y_vel = 0
		self.acceleration_y = 9.8
		self.time_passed = 0.03 #since the last loop
		self.sprite_incrementation = 0.1
		self.create_rect()

        # genetic algorithm
		self.is_alive = True
		self.score = 0
		self.brain = Perceptron()

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
		self.screen.blit(self.sprite[int(self.current_sprite)], (self.x, self.y))

	def clone(self):
		bird = Bird(self.screen)
		# bird.score = self.score
		bird.brain = self.brain
		return bird



class Base():
	def __init__(self, x = 0, y=HEIGHT-50):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, BASE_WIDTH, BASE_HEIGHT)


	def move(self):
		self.x -= BASE_SPEED
		self.rect.x = self.x

	def draw(self, SCREEN):
		SCREEN.blit(BASE_IMAGE,(self.x, self.y))


class Pipe():

	def __init__(self, x, y): # y is for bottom pipe
		self.x = x
		self.y = y
		self.rects = [pygame.Rect(self.x, self.y, PIPE_WIDTH, PIPE_HEIGHT), 
						pygame.Rect(self.x, self.y-PIPE_GAP-PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)] #bottom, top

	def draw(self, SCREEN):
		SCREEN.blit(PIPE_IMAGE, (self.x, self.y)) #bottom
		SCREEN.blit(pygame.transform.rotate(PIPE_IMAGE,180),(self.x, self.y-PIPE_GAP-PIPE_HEIGHT)) #top
		#pygame.draw.rect(SCREEN, (0,0,0), self.rects[0])
		#pygame.draw.rect(SCREEN, (0,0,0), self.rects[1])

	def move(self):
		self.x -= BASE_SPEED 
		for rect in self.rects:
			rect.x = self.x 
