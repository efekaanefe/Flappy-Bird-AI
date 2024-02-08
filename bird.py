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
