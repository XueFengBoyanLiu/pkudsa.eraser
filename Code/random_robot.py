import numpy as np
import random


# 随机选择
class Random:
    def __init__(self):
        pass

    # 随机输出一个解
    def select(self, valid_movement):
        if valid_movement:
            return random.choice(valid_movement)
        return (1, 1), (1, 2)


class Plaser:
    def __init__(self, *args):
        pass

    @ staticmethod
    def move(current_board, valid_movement, *args):
        root = Random()
        return root.select(valid_movement)
