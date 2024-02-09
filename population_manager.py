from game_objects import Bird
from genetic import GeneticAlgorithm
from specie import Specie
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
                bird.score += 1

                # if pipe_list[0].x + PIPE_WIDTH/2 == bird.x:
                #     bird.score += 1

                # dead or alive
                if not check_for_collisions(bird, pipe_list, base_list):
                    bird.is_alive = False

                # features for bird
                x0 = bird.x - pipe_list[0].x # forward
                x1 = bird.y - (pipe_list[0].y - PIPE_GAP) # upward 
                x2 = bird.y - pipe_list[0].y # downward
                x3 = 1 # bias
                X = np.array([x0,x1,x2, x3])

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

    def get_alive_birds_count(self):
        count = 0
        for bird in self.population:
            if bird.is_alive:
                count += 1
        return count

    def survival_of_the_fittest(self):
        self.speciate()

        self.calculate_fitness_for_species()

        self.sort_population()

        # self.generate_next_population()


    def speciate(self):
        for specie in self.species:
            specie.members = []

        for bird in self.population:
            if len(self.species) == 0:
                self.species.append(Specie(bird))

            else:
                bird_is_added_to_members = False

                for specie in self.species:
                    is_bird_relative = specie.is_bird_relative(bird)
                    if is_bird_relative:
                        specie.add_member(bird)
                        bird_is_added_to_members = True
                        break
                        
                if not bird_is_added_to_members: # new specie
                    self.add_new_specie(bird)

    def calculate_fitness_for_species(self):
        for specie in self.species:
            specie.calculate_average_score()
            specie.find_champion()
            
    def sort_population(self): # inside of 
        for specie in self.species:
            specie.sort_members()

        self.species = sorted(self.species, key=lambda specie: specie.average_score, reverse=True)

        # self.population = sorted(self.population, key=lambda bird: bird.score, reverse=True)

    def generate_next_population(self):
        next_generation = []
        for i in range(10):
            bird = Bird(self.screen)
            bird.brain.w = self.population[i]
            bird.brain.b = self.population[i]

        while len(next_generation)<POPULATION_SIZE:
            parents = self.genetic.select_pair(self.population)

            bird_a = Bird(self.screen)
            bird_b = Bird(self.screen)

            # weights and bias
            offspring_a, offspring_b = self.genetic.crossover(parents[0].brain.w, parents[1].brain.w)
            offspring_a = self.genetic.mutation(offspring_a)
            offspring_b = self.genetic.mutation(offspring_b)

            bird_a.brain.w = offspring_a
            bird_b.brain.w = offspring_b

            next_generation += [bird_a, bird_b]

        self.population = next_generation

    def add_new_specie(self, refenrence_bird):
        self.species.append(Specie(refenrence_bird))
        self.species[-1].members.append(refenrence_bird)


