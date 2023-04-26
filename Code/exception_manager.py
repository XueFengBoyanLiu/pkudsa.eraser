import time
import threading
import traceback
import numpy as np

MAXTIME = 0.2
BOARD_SIZE = 8

class Timeout(Exception):
    pass

class InvalidMove(Exception):
    pass

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
    def __init__(self, core, name=''):
        self.name = name
        self.core = core
        self.time = 0
        self.error = None

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
            thread.join(MAXTIME)
            if isinstance(result.state, Exception):
                raise result.state
            self.time += result.state
            if self.time >= MAXTIME:
                raise Timeout()
            if funcname == 'move':
                if not self.is_invalid_move(result.result):
                    raise InvalidMove()
            return result.result
        except:
            if self.error is None:
                self.error = traceback.format_exc()

    def is_invalid_move(self, move) -> bool:
        '''
        This function will check the following:
        - move is a (2, 2) array-like object
        - the two points are adjacent
        - the points lie inside the board
        '''
        try:
            blocks = np.array(move)
            if blocks.shape != (2, 2):
                return False
            distance = np.abs(blocks[0] - blocks[1]).sum()
            if distance != 1:
                return False
            if not ((blocks >= 0) & (blocks < BOARD_SIZE)).all():
                return False
            return True
        except Exception as exception:
            self.error = traceback.format_exc()
            return False

if __name__ == '__main__':
    class tester:
        def __init__(self):
            pass
        def move(self, n, a, b):
            if n == 0.5:
                return ((a,b),(b,a))
            time.sleep(0.01)
            return self.move(n-1, a, b)

    t = tester()
    p = Player_safe(t)
    out = p('move', 19, 7, 6)
    print(out, p.time)
    print(p.error)
