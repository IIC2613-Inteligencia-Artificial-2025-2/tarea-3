# NO TOCAR
CELL = 40
BOARD_SIZE = 9
WALL_THICK = 12
MARGIN = 40

WHITE = (245,245,245)
BLACK = (30,30,30)
LIGHT = (220,200,180)
BLUE = (80,120,200)
RED = (200,80,80)
YELLOW = (230,200,60)

MOVE_UP = (-1,0)
MOVE_DOWN = (1,0)
MOVE_LEFT = (0,-1)
MOVE_RIGHT = (0,1)
MOVES = [MOVE_UP, MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN]

def create_2d(rows, cols, val=False):
    return [[val for _ in range(cols)] for _ in range(rows)]

class PawnPos:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def copy(self):
        return PawnPos(self.r, self.c)
    def __eq__(self, other):
        return self.r==other.r and self.c==other.c

class Pawn:
    def __init__(self, index, is_human_side, board_size, walls_available):
        self.index = index
        self.is_human_side = is_human_side
        start_row = board_size - 1 if is_human_side else 0
        goal_row = 0 if is_human_side else board_size - 1
        start_col = board_size // 2
        self.pos = PawnPos(start_row, start_col)
        self.goal = goal_row
        self.walls_left = walls_available

class Board:
    def __init__(self, human_first=True, size=BOARD_SIZE, walls_per_player=None):
        if size < 3:
            raise ValueError("Board size must be at least 3x3")

        self.size = size
        self.walls_per_player = walls_per_player if walls_per_player is not None else size + 1
        if human_first:
            self.pawns = [Pawn(0, True, size, self.walls_per_player),
                          Pawn(1, False, size, self.walls_per_player)]
            self.human_index = 0
        else:
            self.pawns = [Pawn(0, False, size, self.walls_per_player),
                          Pawn(1, True, size, self.walls_per_player)]
            self.human_index = 1

        span = size - 1
        self.horiz = create_2d(span, span, False)
        self.vert = create_2d(span, span, False)
        self.open_ud = create_2d(span, size, True)
        self.open_lr = create_2d(size, span, True)

    def clone(self):
        b = Board(human_first=(self.human_index == 0), size=self.size, walls_per_player=self.walls_per_player)
        for i in (0,1):
            b.pawns[i].index = self.pawns[i].index
            b.pawns[i].is_human_side = self.pawns[i].is_human_side
            b.pawns[i].pos = self.pawns[i].pos.copy()
            b.pawns[i].goal = self.pawns[i].goal
            b.pawns[i].walls_left = self.pawns[i].walls_left
        b.horiz = [row[:] for row in self.horiz]
        b.vert  = [row[:] for row in self.vert]
        b.open_ud = [row[:] for row in self.open_ud]
        b.open_lr = [row[:] for row in self.open_lr]
        b.human_index = self.human_index
        return b

def in_bounds(r, c, size=BOARD_SIZE):
    return 0 <= r < size and 0 <= c < size
