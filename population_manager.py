from game_objects import Bird
from genetic import GeneticAlgorithm
from constants import *
from game_util import check_for_collisions
import numpy as np


class PopulatioManager:
    def __init__(self, screen):
        self.screen = screen

        self.genetic = GeneticAlgorithm()
        self.population_size = POPULATION_SIZE
        self.generation = 1
        self.population = None
        self.generate_population()
        self.species = []

        self.time_for_decision = INITIAL_TIME_FOR_DECISION # to jump
        
    def generate_population(self):
        self.generation += 1
        self.time_for_decision = INITIAL_TIME_FOR_DECISION
        self.population = [Bird(self.screen) for _ in range(self.population_size)]
    
    def update_population(self, pipe_list, base_list):
        for bird in self.population:
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
                if self.time_for_decision == 0:
                    decision = bird.brain.decision(X)
                    if decision >= 0.5:
                        bird.jump()
                        self.time_for_decision = INITIAL_TIME_FOR_DECISION

                # draw, and update pos
                bird.draw()
                bird.current_sprite += bird.sprite_incrementation
                if int(bird.current_sprite) >= 3:
                    bird.current_sprite = 0
                bird.update_location()


    def survival_of_the_fittest(self, population):
        pass