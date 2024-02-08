import pygame, os, sys, random
from constants import *
from game_objects import Pipe, Base


def draw_base(base_list,SCREEN):
	for i in range(len(base_list)-1,-1,-1):
		base = base_list[i] 
		base.move()
		base.draw(SCREEN)
		if i == 0 and base.x+BASE_WIDTH < -50:
			base.x = base_list[-1].x+BASE_WIDTH-1
			base_list.append(Base(base.x))
			base_list.pop(0)

		 
def draw_pipes(pipe_list,SCREEN):
	for i in range(len(pipe_list)-1,-1,-1):
		pipe = pipe_list[i]
		pipe.move()
		pipe.draw(SCREEN)
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

def draw_score(score, SCREEN):
	text = str(score)
	text_img = SCORE_FONT.render(text, True, (0,0,0))
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2,100+5))
	text_img = SCORE_FONT.render(text, True, (255,255,255))
	SCREEN.blit(text_img, (WIDTH//2-text_img.get_width()//2,100))
	
