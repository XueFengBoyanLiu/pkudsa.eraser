import random


class Random:
    def __init__(self):
        pass

    def select(self, current_board, valid_movement):
        if valid_movement:
            return random.choice(valid_movement)
        pos = (random.randint(1, 6), random.randint(1, 6))
        return pos, (pos[0], pos[1]+1)


class Robot:
    def __init__(self, strategy=Random):
        self.strategy = strategy()

    def move(self, current_board, valid_movement):
        return self.strategy.select(current_board, valid_movement)
