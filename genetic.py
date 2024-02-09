from random import choice, choices, randint, random
from constants import *

# genome here is the perceptron object

class GeneticAlgorithm:
    def __init__(self):
        self.population_size = POPULATION_SIZE
        self.mutations_per_genome = MUTATIONS_PER_GENOME
        self.mutation_probability = MUTATION_PROBABILITY

    # crossover two parent genomes to create two children
    def crossover(self, p1, p2): # single point crossover
        if len(p1) == len(p2):            
            length = len(p1)
            print(p1)
            ci = randint(1, length-1) # crossover index
            return (p1[0:ci] + p2[ci:], p2[0:ci]+p1[ci:])
        else:
            print("parent genomes must be of the same size")

    def mutation(self, genome): 
        genome_copy = genome.copy()
        for _ in range(self.mutations_per_genome):
            if random() <= self.mutation_probability:
                index = randint(0,len(genome)-1)
                mutation_multiplier = choice([-1,1])
                genome_copy[index] = genome_copy[index] + mutation_multiplier * MUTATION_AMOUNT
        return genome_copy

    def evaluate_scores(self, population):
        scores = []
        for bird in population:
            score = bird.score
            scores.append(score)
        return scores

    def select_pair(self, population): 
        weights=[bird.score for bird in population]
        # print(weights)
        return choices(population, weights=weights, k = 2)
    

    def create_baby_from_specie(self, specie):
        baby = specie.members[randint(1, len(specie.members)) - 1].clone()
        baby.brain = self.mutate(baby.brain)
        return baby

    def mutate(self, brain):
        genome = brain.w
        for _ in range(self.mutations_per_genome):
            if random() <= self.mutation_probability:

                index = randint(0,len(genome)-1)
                mutation_multiplier = choice([-1,1])
                mutation_amount = randint(0,101)/100
                genome[index] = genome[index] + mutation_multiplier * mutation_amount #MUTATION_AMOUNT

        brain.w = genome
        return brain
