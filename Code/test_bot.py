import random


class Random:
    def __init__(self):
        pass

    def select(self, current_board, valid_movement):
        if valid_movement:
            return random.choice(valid_movement)
        return (1, 1), (1, 2)


class Robot:
    def __init__(self, strategy=Random):
        self.strategy = strategy()

    def move(self, current_board, valid_movement):
        return self.strategy.select(current_board, valid_movement)
