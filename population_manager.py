from game_objects import Bird
from genetic import GeneticAlgorithm
from specie import Specie
from constants import *
from game_util import check_for_collisions, draw_score
import numpy as np


class PopulatioManager:
    def __init__(self, screen):
        self.screen = screen

        self.genetic = GeneticAlgorithm()
        self.population_size = POPULATION_SIZE
        self.generation = 0
        self.population = None
        self.generate_population()
        self.species = []

        self.highest_score_of_all_time = 0

    def generate_population(self):
        self.generation += 1
        self.current_score = 0
        self.population = [Bird(self.screen) for _ in range(self.population_size)]

    def update_population(self, pipe_list, base_list):
        print("-"*50)
        for bird in self.population:
            if bird.is_alive:
                print(np.random.randint(0,10), bird.y)

                # score
                bird.score += 1

                # if pipe_list[0].x + PIPE_WIDTH/2 == bird.x:
                #     bird.score += 1

                # dead or alive
                if not check_for_collisions(bird, pipe_list, base_list):
                    bird.is_alive = False

                # features for bird
                x0 = bird.x - pipe_list[0].x  # forward
                x1 = bird.y - (pipe_list[0].y - PIPE_GAP)  # upward
                x2 = bird.y - pipe_list[0].y  # downward
                x3 = 1  # bias
                X = np.array([x0, x1, x2, x3])

                # decision to jump
                decision = bird.brain.decision(X)
                if decision >= JUMP_THRESHOLD:
                    bird.jump()

                # draw, and update pos
                bird.draw()
                bird.current_sprite += bird.sprite_incrementation
                if int(bird.current_sprite) >= 3:
                    bird.current_sprite = 0
                bird.update_location()

        # score updates
        scored = False

        if pipe_list[0].x == BIRD_X_INIT:
            self.current_score += 1

        if self.current_score > self.highest_score_of_all_time:
            self.highest_score_of_all_time = self.current_score
        

    def get_alive_birds_count(self):
        count = 0
        for bird in self.population:
            if bird.is_alive:
                count += 1
        return count

    def survival_of_the_fittest(self):  # runs when every bird is dead
        self.speciate()

        self.calculate_fitness_for_species()

        self.sort_population()

        self.generate_next_population()

        self.generation += 1
        self.current_score = 0

    def speciate(self):
        for specie in self.species:
            specie.members = []

        for bird in self.population:
            bird_is_added_to_members = False
            for specie in self.species:
                if specie.is_bird_relative(bird):
                    specie.add_member(bird)
                    bird_is_added_to_members = True
                    break

            if not bird_is_added_to_members:  # new specie
                self.add_new_specie(bird)

        species = []
        for specie in self.species:  # destroy specie if no members
            if len(specie.members) != 0:
                species.append(specie)
        self.species = species

    def calculate_fitness_for_species(self):
        for specie in self.species:
            specie.calculate_average_score()
            specie.find_champion()

    def sort_population(self):  # inside of
        for specie in self.species:
            specie.sort_members()

        self.species = sorted(
            self.species, key=lambda specie: specie.average_score, reverse=True
        )

        # self.population = sorted(self.population, key=lambda bird: bird.score, reverse=True)

    def generate_next_population(self):
        children = []

        for specie in self.species:  # best of every specie survives
            children.append(specie.champion.clone())

        children_per_species = np.floor(
            (self.population_size - len(self.species)) / len(self.species)
        ).astype(int)

        for specie in self.species:
            for i in range(0, children_per_species):
                children.append(self.genetic.create_baby_from_specie(specie))

        while len(children) < self.population_size:  # fill up from best specie
            children.append(self.genetic.create_baby_from_specie(self.species[0]))

        self.population = children

    def add_new_specie(self, refenrence_bird):
        self.species.append(Specie(refenrence_bird))
        self.species[-1].members.append(refenrence_bird)
