import numpy as np
from collections import namedtuple
from time import perf_counter
vec2 = namedtuple("vec2", ("x", "y"))
Operation = namedtuple("Operation", ("pos1", "pos2"))
class Pattern:
    def __init__(self, pattern, operation):
        self.pattern = pattern
        self.operation = operation
    def __repr__(self):
        return f"Pattern(\npattern={self.pattern}, \noperation=\n{self.operation}\n)"
NA = 0
LEVEL = 1200//6
BOARDSIZE = vec2(6, 6*LEVEL)
array = np.array
PATTERNS: dict[vec2: set] = {
    vec2(3, 2): {
        # RIGHT
        Pattern(
            array((
                (1, 0), 
                (0, 1), 
                (0, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(0, 1)
            )
        ), 
        Pattern(
            array((
                (0, 1), 
                (1, 0), 
                (0, 1), 
            )), 
            Operation(
                vec2(1, 0), 
                vec2(1, 1)
            )
        ), 
        Pattern(
            array((
                (0, 1), 
                (0, 1), 
                (1, 0), 
            )), 
            Operation(
                vec2(2, 0), 
                vec2(2, 1)
            )
        ), 
        # LEFT
        Pattern(
            array((
                (0, 1), 
                (1, 0), 
                (1, 0), 
            )), 
            Operation(
                vec2(0, 1), 
                vec2(0, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0), 
                (0, 1), 
                (1, 0), 
            )), 
            Operation(
                vec2(1, 1), 
                vec2(1, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0), 
                (1, 0), 
                (0, 1), 
            )), 
            Operation(
                vec2(2, 1), 
                vec2(2, 0)
            )
        ), 
    }, 
    vec2(1, 4): {
        # RIGHT
        Pattern(
            array((
                (1, 0, 1, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(0, 1)
            )
        ), 
        # LEFT
        Pattern(
            array((
                (1, 1, 0, 1), 
            )), 
            Operation(
                vec2(0, 3), 
                vec2(0, 2)
            )
        ), 
    }, 
    vec2(2, 3): {
        # TOP
        Pattern(
            array((
                (0, 1, 1), 
                (1, 0, 0), 
            )), 
            Operation(
                vec2(1, 0), 
                vec2(0, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0, 1), 
                (0, 1, 0), 
            )), 
            Operation(
                vec2(1, 1), 
                vec2(0, 1)
            )
        ), 
        Pattern(
            array((
                (1, 1, 0), 
                (0, 0, 1), 
            )), 
            Operation(
                vec2(1, 2), 
                vec2(0, 2)
            )
        ), 
        # BOTTOM
        Pattern(
            array((
                (1, 0, 0), 
                (0, 1, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(1, 0)
            )
        ), 
        Pattern(
            array((
                (0, 1, 0), 
                (1, 0, 1), 
            )), 
            Operation(
                vec2(0, 1), 
                vec2(1, 1)
            )
        ), 
        Pattern(
            array((
                (0, 0, 1), 
                (1, 1, 0), 
            )), 
            Operation(
                vec2(0, 2), 
                vec2(1, 2)
            )
        ), 
    }, 
    vec2(4, 1): {
        # TOP
        Pattern(
            array((
                tuple((1, )), 
                tuple((1, )), 
                tuple((0, )), 
                tuple((1, )), 
            )), 
            Operation(
                vec2(3, 0), 
                vec2(2, 0)
            )
        ), 
        # BOTTOM
        Pattern(
            array((
                tuple((1, )), 
                tuple((0, )), 
                tuple((1, )), 
                tuple((1, )), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(1, 0)
            )
        ), 
    }, 
}
def direction(boardshape: vec2, pos: vec2):
    base = {
        vec2( 1,  0), 
        vec2(-1,  0), 
        vec2( 0,  1), 
        vec2( 0, -1), 
    }
    if ( pos.x + 1 ) == boardshape.x:
        base.remove(
            vec2(1, 0)
        )
    if ( pos.y + 1 ) == boardshape.y:
        base.remove(
            vec2(0, 1)
        )
    if pos.x == 0:
        base.remove(
            vec2(-1, 0)
        )
    if pos.y == 0:
        base.remove(
            vec2(0, -1)
        )
    return base

def direction_conn(boardshape: tuple, pos: tuple, connectivity: int):
    base = {
        vec2(-1,  0), 
        vec2( 0, -1), 
    }
    if connectivity == 2:
        base.update({
            vec2(-1,  1), 
            vec2(-1, -1), 
        })
        if pos.x == 0:
            base.remove(
                vec2(-1, 0)
            )
            base.remove(
                vec2(-1, 1)
            )
            base.remove(
                vec2(-1, -1)
            )
        if ( pos.y + 1 ) == boardshape.y:
            if pos.x != 0:
                base.remove(
                    vec2(-1, 1)
                )
        if pos.y == 0:
            base.remove(
                vec2(0, -1)
            )
            if pos.x != 0:
                base.remove(
                    vec2(-1, -1)
                )
        return base
    if pos.x == 0:
        base.remove(
            vec2(-1, 0)
        )
    if pos.y == 0:
        base.remove(
            vec2(0, -1)
        )
    return base
class ScoredBoard:
    def __init__(self, select_hist, score_hist, score, board, operation):
        self.select_hist = select_hist
        self.score_hist = score_hist
        self.score = score
        self.board = board
        self.operation = operation
    def __repr__(self):
        return f"ScoreBoard(\nselect_hist={self.select_hist}, \nscore_hist={self.score_hist}, \nscore={self.score}, \nboard=\n{self.board}, \noperation=\n{self.operation}\n)"
class BoardManager:
    def __init__(self, is_first: bool = None) -> None:
        _ = is_first
    scoreboards: list[set[ScoredBoard]] = list()
    mapper = {
        'R': 1, 
        'B': 2, 
        'G': 3, 
        'Y': 4, 
        'P': 5, 
    }
    def _init(self, board, availables):
        observation: np.ndarray = board[:BOARDSIZE.x, :BOARDSIZE.y]
        for key, value in self.mapper.items():
            observation[ observation == key ] = value
        observation = observation.astype(np.int8)
        self.scoreboards.append([
            ScoredBoard(
                [], 
                [], 
                0, 
                observation, 
                None, 
            ), 
        ])
    def _find_next_level(self, select: int, scoreboard: ScoredBoard) -> list[np.ndarray]:
        fullboard = scoreboard.board
        board = fullboard[:BOARDSIZE.x, :BOARDSIZE.x]
        possibles = self._find_movables(board)
        return [
            self._move(select, scoreboard, board, operation) for operation in possibles
        ]
    def _move(self, select: int, scoreboard: ScoredBoard, board: np.ndarray, operation: Operation):
        operation, pattern = operation # DEBUG
        pos1, pos2 = operation
        new = board.copy()
        new[pos1] = board[pos2]
        new[pos2] = board[pos1]
        erasedboard, erased = self._erase(new, pos2)
        fullboard = self._update_fullboard(scoreboard.board, erasedboard)
        erased_score = self._heuristic(erased)
        return ScoredBoard(
            scoreboard.select_hist + [select], 
            scoreboard.score_hist + [erased_score], 
            scoreboard.score + ( 0 if self.level % 2 else erased_score ), 
            fullboard, 
            operation, 
        )
    def _update_fullboard(self, fullboard: np.ndarray, board: np.ndarray):
        fullboard = fullboard.copy()
        fullboard[:BOARDSIZE.x, :BOARDSIZE.x] = board
        for i in range(BOARDSIZE.x):
            fullboard[i] = np.concatenate((
                fullboard[i][ fullboard[i]!=NA ], 
                np.zeros(
                    (BOARDSIZE.y - (fullboard[i][ fullboard[i]!=NA ]).shape[0], ), 
                    dtype=np.int8
                )
            ))
        return fullboard
    def _erase(self, board: np.ndarray, pos: vec2, erased=0) -> tuple[np.ndarray, int]:
        target = board[pos]
        board[pos] = NA
        erased += 1
        for d in direction(vec2(*board.shape), pos):
            newpos = vec2(
                pos.x + d.x, 
                pos.y + d.y
            )
            if board[newpos] == target:
                board, erased = self._erase(board, newpos, erased=erased)
        return board, erased
    def _find_movables(self, board: np.ndarray) -> list[Operation]:
        labeled = self._label(board, connectivity=2)
        clustered_indexes = [
            np.where(labeled == label)
            for label in np.unique(labeled)
            if label != NA
        ]
        possibles = self._filter_not_removable(clustered_indexes)
        return possibles
    def _label(self, board: np.ndarray, connectivity: int) -> np.ndarray:
        no = 1
        boardshape = vec2(*board.shape)
        new = np.zeros(boardshape, dtype=np.int8)
        for element in self.mapper.values():
            is_element: np.ndarray = np.array( board == element , dtype=np.int8 )
            _x, _y = is_element.shape
            for x in range(_x):
                for y in range(_y):
                    labeled = False
                    if is_element[x][y]:
                        for d in direction_conn(boardshape, vec2(x,y), connectivity):
                            if is_element[x+d.x][y+d.y]:
                                is_element[x][y] = is_element[x+d.x][y+d.y]
                                labeled = True
                                break
                        if not labeled:
                            is_element[x][y] = no
                            no += 1
            new = new + is_element
        return new
    def _filter_not_removable(self, clustered_indexes) -> list[Operation]:
        possibles = []
        for i, clustered_index in enumerate(clustered_indexes):
            if self.halt:
                break
            if len( clustered_index[0] ) >= 3:
                xmin, ymin, xmax, ymax = (
                    np.min(clustered_index[0]), 
                    np.min(clustered_index[1]), 
                    np.max(clustered_index[0]), 
                    np.max(clustered_index[1]), 
                )
                cluster_pattern = np.zeros((xmax-xmin+1, ymax-ymin+1), dtype=np.int8)
                for x, y in zip(*clustered_index):
                    cluster_pattern[x-xmin, y-ymin] = 1
                cluster_x, cluster_y = cluster_pattern.shape
                for shape, patterns in PATTERNS.items():
                    if ( ( perf_counter() - self.t0 ) > 0.09 ):
                        self.halt = True
                        break
                    if shape.x <= cluster_x and shape.y <= cluster_y:
                        for pattern in patterns:
                            flatpattern = pattern.pattern.flatten()
                            for x in range( cluster_x - shape.x + 1 ):
                                for y in range( cluster_y - shape.y + 1 ):
                                    current = cluster_pattern[x:x+shape.x, y:y+shape.y]
                                    if ( flatpattern == current.flatten() ).all():
                                        operation = Operation(
                                            vec2(
                                                pattern.operation.pos1.x + x + xmin, 
                                                pattern.operation.pos1.y + y + ymin
                                            ), 
                                            vec2(
                                                pattern.operation.pos2.x + x + xmin, 
                                                pattern.operation.pos2.y + y + ymin
                                            ), 
                                        )
                                        possibles.append(
                                            ( operation, pattern.pattern )
                                        )
        return possibles
    def _heuristic(self, erased: int) -> int:
        return ( erased - 2 ) ** 2
    def _run(self):
        self.halt = False
        self.level = -1
        while ( not self.halt ):
            if not self.scoreboards[ self.level + 1 ]:
                print("\n\n  Stopped because No Effective Action to Perform\n\n")
                break
            self.level += 1
            self.scoreboards.append( list() )
            for select, scoreboard in enumerate( self.scoreboards[self.level] ):
                self.scoreboards[ self.level + 1 ].extend(
                    self._find_next_level(select, scoreboard)
                )
            self.scoreboards[ self.level + 1 ] = sorted(
                self.scoreboards[ self.level + 1 ], 
                key=lambda scoreboard: sum(scoreboard.score_hist), 
                reverse=True
            )[:( -1 if self.level % 2 else 1)]
            print(f"  Level {self.level:02d} -> {self.level+1:02d} :: Time consumed : {perf_counter()-self.t0:.6f} seconds")
            if ( ( perf_counter() - self.t0 ) > .09 ):
                self.halt = True
        if not self.scoreboards[ self.level + 1 ]:
            self.scoreboards.pop(self.level + 1)
    def _traceback(self) -> Operation:
        print(f"{self.scoreboards=}")
        best: ScoredBoard = self.scoreboards[-1][0]
        if best.select_hist:
            root: ScoredBoard = self.scoreboards[1][best.select_hist[0]]
        else:
            root = self.scoreboards[0][0]
        return root.operation
    @staticmethod
    def _convert(operation: Operation) -> tuple[tuple, tuple]:
        print(operation)
        return (
            (
                operation.pos1.x, 
                operation.pos1.y
            ), 
            (
                operation.pos2.x, 
                operation.pos2.y
            )
        )
    def move(self, board, availables, score, turn):
        
        self.t0 = perf_counter()
        
        self._init(board, availables)
        self._run()
        
        operation = self._traceback()
        operation = self._convert(operation)
        
        if operation in availables:
            return operation
        else:
            return operation[::-1]