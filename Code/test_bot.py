import random
from eraserconfig import *

class Random:
    def __init__(self):
        pass

    def select(self, current_board, valid_movement):
        if valid_movement:
            return random.choice(valid_movement)
        pos = (random.randint(0, BOARD_SIZE - 2), random.randint(0, BOARD_SIZE - 2))
        return pos, (pos[0], pos[1]+1)


class Plaser:
    def __init__(self, strategy=Random):
        self.strategy = strategy()

    def move(self, current_board, valid_movement, *args):
        return self.strategy.select(current_board, valid_movement)
