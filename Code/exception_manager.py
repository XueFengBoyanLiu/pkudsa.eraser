import time
import threading
import traceback
import numpy as np

from eraserconfig import *

class Timeout(Exception):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return 'Time limit exceeded.'

class InvalidMove(Exception):
    def __init__(self, message):
        super().__init__()
        self.error_message = message
    def __str__(self):
        return self.error_message

class Caller:
    def __init__(self, func):
        self.func = func
        self.result = None
        self.state = Timeout()

    def call(self, *args, **kwargs):
        try:
            begin = time.perf_counter()
            self.result = self.func(*args, **kwargs)
            end = time.perf_counter()
            self.state = end - begin
        except Exception as exception:
            self.state = exception

class Player_safe:
    def __init__(self, core, *args):
        self.error = None
        try:
            self.core = core(*args)
        except:
            self.error = traceback.format_exc()
        self.time = 0

    def __call__(self, funcname, *args, **kwargs):
        '''Call the 'funcmane' method of the core class
        It will check the following:
        - Time limit
        - When calling 'move' method, assert the move is valid
        If the above assertions fail or an error occurred,
        the error traceback will stored in self.error
        '''
        self.output = None
        if self.error is not None:
            return
        try:
            result = Caller(getattr(self.core, funcname))
            thread = threading.Thread(target=result.call,
                    args=(*args,), kwargs={**kwargs})
            thread.daemon = True
            thread.start()
            thread.join(MAX_TIME - self.time)
            if isinstance(result.state, Exception):
                raise result.state
            self.time += result.state
            if self.time >= MAX_TIME:
                raise Timeout()
            if funcname == 'move':
                self.check_for_invalid_move(result.result)
            return result.result
        except:
            self.error = traceback.format_exc()

    def check_for_invalid_move(self, move):
        '''
        This function will check the following:
        - move is a (2, 2) array-like object
        - the two points are adjacent
        - the points lie inside the board
        '''
        if len(move) != 2 or len(move[0]) != 2 or len(move[1]) != 2:
            raise InvalidMove('Not a proper input.')
        blocks = np.array(move)
        distance = np.abs(blocks[0] - blocks[1]).sum()
        if distance != 1:
            raise InvalidMove('Not adjacent positions.')
        if not ((blocks >= 0) & (blocks < BOARD_SIZE)).all():
            raise InvalidMove('Positions out of board.')
