import time
import random
'''
大约第十次左右报错
FailedRobot1:超100ms限时
FailedRobot2:错误格式输出
FailedRobot3:非法移动输出
FailedRobot4:没有move方法
FailedRobot5:运行过程出错
'''


class Plaser:
    def __init__(self, *args):
        pass

    def move(self, current_board, valid_movement, *args):
        t = time.time()
        max_t = 0.01
        if random.random() > 0.9:
            max_t = 100
        while time.time() - t < max_t:
            i = 0
        return (1, 1), (1, 2)


class Bot2:
    def __init__(self, *args):
        pass

    def move(self, current_board, valid_movement, *args):
        if random.random() > 0.98:
            return (1, 1), (1, )
        if random.random() > 0.98:
            return (1, 2, 3), (1, 2)
        if random.random() > 0.98:
            return (1, 1), (1, 1), (1, 2)
        if random.random() > 0.98:
            return '(1, 1), (1, 2)'
        if random.random() > 0.98:
            return 114514
        return (1, 1), (1, 2)


class FailedRobot3:
    def __init__(self):
        pass

    def move(self, current_board, valid_movement):
        if random.random() > 0.95:
            return (1, 1), (4, 7)
        if random.random() > 0.95:
            return (1, 7), (1, 8)
        return (1, 1), (1, 2)


class FailedRobot4:
    def __init__(self):
        pass


class FailedRobot5:
    def __init__(self):
        pass

    def move(self, current_board, valid_movement):
        if random.random() > 0.95:
            x = 0
            ans = x + 1 / x
        if random.random() > 0.95:
            l = []
            del l[0]
        return (1, 1), (1, 2)
