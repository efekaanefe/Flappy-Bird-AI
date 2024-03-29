import pygame.font
pygame.font.init()


SCORE_FONT =pygame.font.SysFont("comicsans", 100)
INFO_FONT =pygame.font.SysFont("comicsans", 28)

WIDTH = 600
HEIGHT = 800

BASE_WIDTH, BASE_HEIGHT = 400, 200
BASE_SPEED = 5 # 10 % base_speed must be equal to 0, otherwise scoring mechanism won´t work properly


PIPE_WIDTH, PIPE_HEIGHT = 100, 600
PIPE_GAP = 150 # vertical
PIPE_DISTANCE = 400 # horizontal
PIPE_LOWER_HEIGHT_BOUND = 300
PIPE_UPPER_HEIGHT_BOUND = 650


BIRD_SCALE = 1.5
BIRD_WIDTH, BIRD_HEIGHT =  int(34*BIRD_SCALE), int(24*BIRD_SCALE)

BASE_IMAGE = pygame.transform.scale(pygame.image.load("assets/base.png"), (BASE_WIDTH,BASE_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/bg.png"), (WIDTH,HEIGHT))
PIPE_IMAGE = pygame.transform.scale(pygame.image.load("assets/pipe.png"), (PIPE_WIDTH, PIPE_HEIGHT))
BIRD_SPRITE = []
for i in range(3): BIRD_SPRITE.append(pygame.transform.scale(pygame.image.load(f"assets/bird{i}.png"), (BIRD_WIDTH, BIRD_HEIGHT)))

BIRD_X_INIT = 25
BIRD_Y_INIT = 400


# Genetic
POPULATION_SIZE = 100
MUTATIONS_PER_GENOME = 3
MUTATION_PROBABILITY = 0.5
MUTATION_AMOUNT  = 0.1
WEIGHT_DIFFERENCE_THRESHOLD = 2

JUMP_THRESHOLD = 0.5

