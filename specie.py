import numpy as np
from constants import WEIGHT_DIFFERENCE_THRESHOLD


class Specie:
    def __init__(self, refenrence_bird):
        self.refenrence_bird = refenrence_bird
        self.reference_weights = refenrence_bird.brain.w
        self.members = []
        self.members.append(refenrence_bird)
        self.average_score = 0
        self.champion = None # per gen

    def is_bird_relative(self, new_bird):
        new_weights = new_bird.brain.w
        total_weight_difference = np.abs(np.sum(new_weights-self.reference_weights))
        if total_weight_difference<WEIGHT_DIFFERENCE_THRESHOLD:
            return True
        return False

    def add_member(self, bird):
        self.members.append(bird)
    
    def calculate_average_score(self):
        if len(self.members) != 0:
            sum = 0
            for member in self.members:
                sum += member.score
            self.average_score = sum / len(self.members)
        else:
            self.average_score = 0

    def sort_members(self):
        self.members = sorted(self.members, key=lambda bird: bird.score, reverse=True)

    def find_champion(self):
        max_score = 0
        for bird in self.members:
            if bird.score > max_score:
                self.champion = bird
                max_score = bird.score
        if max_score == 0:
            self.champion = self.members[0]