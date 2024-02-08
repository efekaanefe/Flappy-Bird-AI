from bird import Bird
from genetic import GeneticAlgorithm


class PopulatioManager:
    def __init__(self, 
                 population_size, 
                 mutations_per_genome, 
                 mutation_probability,
                 screen
                ):
        
        self.population_size = population_size
        self.screen = screen

        self.genetic = GeneticAlgorithm(population_size,
                                        mutations_per_genome,
                                        mutation_probability)
        self.generation = 1
        
    def generate_population(self):
        return [Bird(self.screen) for _ in range(self.population_size)]

    def survival_of_the_fittest(self, population):
        pass