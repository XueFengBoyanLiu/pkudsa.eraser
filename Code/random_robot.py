import numpy as np


# 随机选择
class Random:
    def __init__(self):
        pass

    # 随机输出一个解
    def select(self, valid_movement):
        if valid_movement:
            return valid_movement[np.random.randint(0, len(valid_movement))]
        return (1, 1), (1, 2)


class RandomRobot:
    def __init__(self):
        pass

    @ staticmethod
    def move(current_board, valid_movement):
        root = Random()
        return root.select(valid_movement)
