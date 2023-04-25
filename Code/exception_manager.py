import time
import threading
import traceback

MAXTIME = 1000

class Timeout(Exception):
    pass

class Call:
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

class Player:
    def __init__(self, core, name=''):
        self.name = name
        self.core = core
        self.time = 0
        self.error = None

    def __call__(self, funcname, *args, **kwargs):
        self.output = None
        if self.error is not None:
            return
        try:
            result = Call(getattr(self.core, funcname))
            thread = threading.Thread(target=result.call,
                    args=(*args,), kwargs={**kwargs})
            thread.daemon = True
            thread.start()
            thread.join(MAXTIME - self.time)
            if isinstance(result.state, Exception):
                raise result.state
            self.time += result.state
            if self.time >= MAXTIME:
                raise Timeout()
            return result.result
        except:
            self.error = traceback.format_exc()
