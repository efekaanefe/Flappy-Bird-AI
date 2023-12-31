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

BASE_IMAGE = pygame.transform.scale(pygame.image.load("assets/base.png"), (BASE_WIDTH,BASE_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/bg.png"), (WIDTH,HEIGHT))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load("assets/pipe.png"), (PIPE_WIDTH, PIPE_HEIGHT))
BIRD_SPRITE = []
for i in range(3): BIRD_SPRITE.append(pygame.transform.scale(pygame.image.load(f"assets/bird{i}.png"), (BIRD_WIDTH, BIRD_HEIGHT)))
