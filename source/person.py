import random

from numpy.random import choice


class Person:
    def __init__(self, x_range: tuple[int, int], y_range: tuple[int, int], healthy_start_percentage: float,
                 sick_start_percentage: float, infection_chance: float, immune_chance: float):
        self.x_range = x_range
        self.y_range = y_range
        self.x_position = random.randint(*self.x_range)
        self.y_position = random.randint(*self.y_range)
        self.speed = 0
        self.test_result = choice(['h', 's'], p=[healthy_start_percentage, sick_start_percentage])
        self.move_target = ()
        self.set_move_target()

        self.infection_chance = infection_chance
        self.immune_chance = immune_chance

    def set_move_target(self):
        self.move_target = (random.randint(*self.x_range), random.randint(*self.y_range))
        self.speed = choice([1, 1.5, 2], p=[0.5, 0.3, 0.2])

    def move(self):
        # get a new move target if already at current one
        if self.x_position - self.speed <= self.move_target[0] <= self.x_position + self.speed:
            if self.y_position - self.speed <= self.move_target[1] <= self.y_position + self.speed:
                self.set_move_target()

        # find distance in both axes
        x_distance = self.move_target[0] - self.x_position
        y_distance = self.move_target[1] - self.y_position

        # determine direction for person to go
        if abs(x_distance) >= abs(y_distance):
            if x_distance > 0:
                self.x_position += self.speed
            else:
                self.x_position -= self.speed
        else:
            if y_distance > 0:
                self.y_position += self.speed
            else:
                self.y_position -= self.speed

    def collision(self):
        # random chance for healthy to become sick
        if self.test_result == 'h':
            if random.randint(1, int(1 // self.infection_chance)) == 1:
                self.test_result = 's'

    def tick(self):
        # random chance for sick to become immune
        if self.test_result == 's':
            if random.randint(1, int(1 // self.immune_chance)) == 1:
                self.test_result = 'i'
