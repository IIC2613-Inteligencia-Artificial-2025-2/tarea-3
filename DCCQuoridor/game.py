# NO TOCAR
import copy
from board import Board, PawnPos, MOVES, BOARD_SIZE
import algorithms

class Game:
    def __init__(self, human_first=True, pathfinder='astar', board_size=BOARD_SIZE):
        self.board = Board(human_first, size=board_size)
        self.turn = 0
        self.winner = None
        self.history = []
        self.pathfinder = pathfinder
        self.board_size = self.board.size

    def set_pathfinder(self, pathfinder):
        if pathfinder in ['bfs', 'astar']:
            self.pathfinder = pathfinder
        else:
            raise ValueError("Pathfinder must be 'bfs' or 'astar'")
        
    def pawn_of_turn(self):
        return self.board.pawns[self.turn % 2]

    def pawn_not_turn(self):
        return self.board.pawns[(self.turn + 1) % 2]

    def clone(self):
        human_first = (self.board.human_index == 0) if hasattr(self.board, "human_index") else True
        g = Game(human_first=human_first, pathfinder=self.pathfinder, board_size=self.board.size)
        g.board = self.board.clone()
        g.turn = self.turn
        g.winner = None if self.winner is None else g.board.pawns[self.winner.index]
        g.history = copy.deepcopy(self.history)
        g.board_size = g.board.size
        return g

    # --- Movimiento de peones ---
    def valid_next_positions(self):
        size = self.board.size
        res = [[False] * size for _ in range(size)]
        p = self.pawn_of_turn().pos
        opp = self.pawn_not_turn().pos

        for main, s1, s2 in [
            (MOVES[0], MOVES[1], MOVES[2]),
            (MOVES[3], MOVES[1], MOVES[2]),
            (MOVES[1], MOVES[0], MOVES[3]),
            (MOVES[2], MOVES[0], MOVES[3])
        ]:
            if self.is_open(p.r, p.c, main):
                mpos = PawnPos(p.r + main[0], p.c + main[1])
                if mpos == opp:
                    if self.is_open(mpos.r, mpos.c, main):
                        mm = PawnPos(mpos.r + main[0], mpos.c + main[1])
                        res[mm.r][mm.c] = True
                    else:
                        if self.is_open(mpos.r, mpos.c, s1):
                            s = PawnPos(mpos.r + s1[0], mpos.c + s1[1])
                            res[s.r][s.c] = True
                        if self.is_open(mpos.r, mpos.c, s2):
                            s = PawnPos(mpos.r + s2[0], mpos.c + s2[1])
                            res[s.r][s.c] = True
                else:
                    res[mpos.r][mpos.c] = True
        return res

    def move_pawn(self, r, c):
        valid = self.valid_next_positions()
        if not valid[r][c]:
            return False
        p = self.pawn_of_turn()
        p.pos.r = r
        p.pos.c = c
        if p.pos.r == p.goal:
            self.winner = p
        self.turn += 1
        return True

    # --- Validación y colocación de paredes ---
    def is_open(self, r, c, move):
        dr, dc = move
        size = self.board.size
        if (dr, dc) == MOVES[0]: return r > 0 and self.board.open_ud[r-1][c]
        if (dr, dc) == MOVES[3]: return r < size - 1 and self.board.open_ud[r][c]
        if (dr, dc) == MOVES[1]: return c > 0 and self.board.open_lr[r][c-1]
        if (dr, dc) == MOVES[2]: return c < size - 1 and self.board.open_lr[r][c]
        return False

    def can_place_horiz(self, row, col):
        span = self.board.size - 1
        if not (0 <= row < span and 0 <= col < span): 
            return False
        if self.board.horiz[row][col]: 
            return False
        # paredes horizontales adyacentes
        if col > 0 and self.board.horiz[row][col-1]: return False
        if col < span - 1 and self.board.horiz[row][col+1]: return False
        # paredes verticales que crucen
        if self.board.vert[row][col]: return False
        if col + 1 < span and self.board.vert[row][col+1]: return False  # <-- corregido
        if self.pawn_of_turn().walls_left <= 0: return False
        # colocar temporalmente y verificar caminos
        self.board.horiz[row][col] = True
        prev1 = self.board.open_ud[row][col]
        prev2 = self.board.open_ud[row][col+1]
        self.board.open_ud[row][col] = False
        self.board.open_ud[row][col+1] = False
        ok = self.paths_exist_for_both()
        # revertir
        self.board.horiz[row][col] = False
        self.board.open_ud[row][col] = prev1
        self.board.open_ud[row][col+1] = prev2
        return ok



    def can_place_vert(self, row, col):
        span = self.board.size - 1
        if not (0 <= row < span and 0 <= col < span): return False
        if self.board.vert[row][col]: return False
        # verticales adyacentes
        if row > 0 and self.board.vert[row-1][col]: return False
        if row < span - 1 and self.board.vert[row+1][col]: return False
        # horizontales que crucen
        if self.board.horiz[row][col]: return False
        if row + 1 < span and self.board.horiz[row+1][col]: return False  # <-- corregido
        if self.pawn_of_turn().walls_left <= 0: return False
        # temporal y verificar caminos
        self.board.vert[row][col] = True
        prev1 = self.board.open_lr[row][col]
        prev2 = self.board.open_lr[row+1][col]
        self.board.open_lr[row][col] = False
        self.board.open_lr[row+1][col] = False
        ok = self.paths_exist_for_both()
        self.board.vert[row][col] = False
        self.board.open_lr[row][col] = prev1
        self.board.open_lr[row+1][col] = prev2
        return ok



    def place_horiz(self, row, col):
        if not self.can_place_horiz(row, col): return False
        self.board.horiz[row][col] = True
        self.board.open_ud[row][col] = False
        self.board.open_ud[row][col+1] = False
        self.pawn_of_turn().walls_left -= 1
        self.turn +=1
        return True

    def place_vert(self, row, col):
        if not self.can_place_vert(row, col): return False
        self.board.vert[row][col] = True
        self.board.open_lr[row][col] = False
        self.board.open_lr[row+1][col] = False
        self.pawn_of_turn().walls_left -=1
        self.turn +=1
        return True

    # --- Caminos ---
    def paths_exist_for_both(self):
        for pawn in self.board.pawns:
            if not self._has_path(pawn): return False
        return True
    
    def _has_path(self, pawn):
        start = (pawn.pos.r, pawn.pos.c)
        goal_row = pawn.goal
        if self.pathfinder == 'bfs':
            found, _ = algorithms.bfs_to_goal_row(self, start, goal_row)
        else: 
            found, _ = algorithms.astar_to_goal_row(self, start, goal_row)
        return found
    
    # --- Movimientos legales ---
    def get_all_moves(self, wall_radius=None):
        moves = []
        val = self.valid_next_positions()
        size = self.board.size
        for r in range(size):
            for c in range(size):
                if val[r][c]: moves.append(('move',(r,c)))

        # Paredes solo si el jugador actual aún le quedan paredes
        wl = self.pawn_of_turn().walls_left
        if wl <= 0: return moves

        p0, p1 = self.board.pawns[0].pos, self.board.pawns[1].pos
        if wall_radius is None:
            wall_radius = max(6, size)
        for r in range(size - 1):
            for c in range(size - 1):
                if abs(r-p0.r)+abs(c-p0.c) > wall_radius and \
                   abs(r-p1.r)+abs(c-p1.c) > wall_radius: 
                    continue
                if self.can_place_horiz(r,c):
                    moves.append(('hwall',(r,c)))
                if self.can_place_vert(r,c):
                    moves.append(('vwall',(r,c)))
        return moves

    # --- Distancia ---
    def shortest_distance_for(self, pawn_index):
        pawn = self.board.pawns[pawn_index]
        start = (pawn.pos.r, pawn.pos.c)
        goal_row = pawn.goal
        if self.pathfinder == "astar":
            found, dist = algorithms.astar_to_goal_row(self, start, goal_row)
        else:
            found, dist = algorithms.bfs_to_goal_row(self, start, goal_row)
        return dist if found else 9999
