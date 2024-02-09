import numpy as np
from constants import WEIGHT_DIFFERENCE_THRESHOLD
class Specie:
    def __init__(self, refenrence_bird):
        self.refenrence_bird = refenrence_bird
        self.reference_weights = refenrence_bird.brain.w
        self.members = []
        self.average_score = 0

    def is_bird_relative(self, new_bird):
        new_weights = new_bird.brain.w
        total_weight_difference = np.sum(new_weights-self.reference_weights)
        if total_weight_difference<WEIGHT_DIFFERENCE_THRESHOLD:
            return True
        return False

    def add_member(self, bird):
        self.members.append(bird)
    
    def calculate_average_score(self):
        sum = 0
        for member in self.members:
            sum += member.score
        self.average_score = sum / len(self.members)

    def sort_members(self):
        self.members = sorted(self.members, key=lambda bird: bird.score, reverse=True)