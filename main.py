import pygame, os, sys, random
import pygame.font

pygame.font.init()

SCORE_FONT =pygame.font.SysFont("comicsans", 100)

WIDTH = 500
HEIGHT = 800

BASE_WIDTH, BASE_HEIGHT = 400, 200
BASE_SPEED = 5 # 10 % base_speed must be equal to 0, otherwise scoring mechanism won´t work properly

PIPE_WIDTH, PIPE_HEIGHT = 100, 600
PIPE_GAP = 200 #vertical
PIPE_DISTANCE = 250 #horizontal
PIPE_LOWER_HEIGHT_BOUND = 300
PIPE_UPPER_HEIGHT_BOUND = 650

BIRD_SCALE = 1.5
BIRD_WIDTH, BIRD_HEIGHT =  int(34*BIRD_SCALE), int(24*BIRD_SCALE)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BASE_IMAGE = pygame.transform.scale(pygame.image.load("assets/base.png"), (BASE_WIDTH,BASE_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/bg.png"), (WIDTH,HEIGHT))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load("assets/pipe.png"), (PIPE_WIDTH, PIPE_HEIGHT))
BIRD_SPRITE = []
for i in range(3): BIRD_SPRITE.append(pygame.transform.scale(pygame.image.load(f"assets/bird{i}.png"), (BIRD_WIDTH, BIRD_HEIGHT)))

def main():
	clock = pygame.time.Clock()
	run = True
	start = False
	score = 0 
	base_list = [Base(0), Base(BASE_WIDTH), Base(2*BASE_WIDTH)]
	pipe_list = [Pipe(WIDTH,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+PIPE_WIDTH+PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND)), 
				 Pipe(WIDTH+2*PIPE_WIDTH+2*PIPE_DISTANCE,random.randint(PIPE_LOWER_HEIGHT_BOUND, PIPE_UPPER_HEIGHT_BOUND))]
	bird = Bird()
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
				elif event.key == pygame.K_SPACE:
					start = True
					bird.jump()

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
			print("Restarting Game")
			pygame.time.delay(1000)

			main()

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
	main()

