# NO TOCAR
import pygame
import sys
import copy
import time
from game import Game
from minimax import minimax
from board import MOVES, BOARD_SIZE, CELL, WALL_THICK, MARGIN, WHITE, BLACK, LIGHT, BLUE, RED, YELLOW

FPS = 30

pygame.init()
FONT = pygame.font.SysFont(None, 20)


def compute_window_size(board_size):
    board_pixels = CELL * board_size + WALL_THICK * (board_size - 1)
    width = MARGIN * 2 + board_pixels
    height = width + 80
    return width, height


class UI:
    def __init__(self, player1, player2, pathfinder="astar", board_size=BOARD_SIZE, headless=False):
        self.players = [player1, player2]
        # Headless SOLO si ambos no son humanos y el caller lo pidió
        self.headless = headless and (not player1.is_human) and (not player2.is_human)

        self.board_size = board_size
        self.window_w, self.window_h = compute_window_size(board_size)

        # no abrir ninguna ventana antes de decidir el modo
        if self.headless:
            # Headless: no creamos ventana; sólo un Clock si quieres compasar
            self.screen = None
            self.clock = pygame.time.Clock()
        else:
            # Con UI: creamos ventana visible
            self.screen = pygame.display.set_mode((self.window_w, self.window_h))
            pygame.display.set_caption("Quoridor")
            self.clock = pygame.time.Clock()

        self.game = Game(human_first=True, pathfinder=pathfinder, board_size=board_size)
        self.selected_mode = 'move'
        self.running = True
        self.history = []
        self.total_time = [0.0, 0.0]

        # Si comienza la IA, dispara su turno según el modo
        if not self.players[self.game.turn % 2].is_human:
            if self.headless:
                self.ai_move_for_player(self.players[self.game.turn % 2])
            else:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    def board_to_pixel(self, r,c):
        x = MARGIN + c*CELL + c*WALL_THICK
        y = MARGIN + r*CELL + r*WALL_THICK
        return x,y

    def pixel_to_cell(self, x,y):
        if x < MARGIN or y < MARGIN:
            return None
        x0 = x - MARGIN
        y0 = y - MARGIN
        block_w = CELL+WALL_THICK
        c = x0 // block_w
        r = y0 // block_w
        if r >= self.board_size or c >= self.board_size:
            return None
        lx = x0 % block_w
        ly = y0 % block_w
        if lx < CELL and ly < CELL:
            return ('cell', int(r), int(c))
        if lx >= CELL and ly < CELL:
            return ('vslot', int(r), int(c))
        if ly >= CELL and lx < CELL:
            return ('hslot', int(r), int(c))
        return None

    def draw(self):
        if self.headless:
            return # No dibujar nada en modo headless
        
        self.screen.fill(WHITE)
        # draw cells
        for r in range(self.board_size):
            for c in range(self.board_size):
                x,y = self.board_to_pixel(r,c)
                pygame.draw.rect(self.screen, LIGHT, (x,y,CELL,CELL))
                pygame.draw.rect(self.screen, BLACK, (x,y,CELL,CELL),1)
        # draw walls
        for r in range(self.board_size - 1):
            for c in range(self.board_size - 1):
                if self.game.board.horiz[r][c]:
                    x,y = self.board_to_pixel(r,c)
                    wx = x; wy = y+CELL
                    w_w = CELL*2 + WALL_THICK
                    pygame.draw.rect(self.screen, BLACK, (wx,wy-WALL_THICK//2,w_w,WALL_THICK))
                if self.game.board.vert[r][c]:
                    x,y = self.board_to_pixel(r,c)
                    vx = x+CELL; vy=y
                    h_h = CELL*2 + WALL_THICK
                    pygame.draw.rect(self.screen, BLACK, (vx-WALL_THICK//2,vy,WALL_THICK,h_h))
        # highlight valid moves for human
        current_player = self.players[self.game.turn%2]
        if current_player.is_human and self.selected_mode=='move':
            val = self.game.valid_next_positions()
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if val[r][c]:
                        x,y = self.board_to_pixel(r,c)
                        pygame.draw.rect(self.screen, YELLOW, (x+5,y+5,CELL-10,CELL-10),2)

        # === DEBUG VISUAL DE SLOTS DE MURALLA COLOCABLES ===
        current_player = self.players[self.game.turn%2]
        if current_player.is_human:
            wl = self.game.pawn_of_turn().walls_left
            # HORIZONTALES
            if self.selected_mode == 'hwall' and wl>0:
                for r in range(self.board_size - 1):
                    for c in range(self.board_size - 1):
                        if self.game.can_place_horiz(r, c):
                            x, y = self.board_to_pixel(r, c)
                            wx = x; wy = y + CELL
                            w_w = CELL*2 + WALL_THICK
                            # “fantasma” amarillo
                            pygame.draw.rect(self.screen, YELLOW, (wx, wy - WALL_THICK//2, w_w, WALL_THICK), 2)

            # VERTICALES
            if self.selected_mode == 'vwall' and wl>0:
                for r in range(self.board_size - 1):
                    for c in range(self.board_size - 1):
                        if self.game.can_place_vert(r, c):
                            x, y = self.board_to_pixel(r, c)
                            vx = x + CELL; vy = y
                            h_h = CELL*2 + WALL_THICK
                            pygame.draw.rect(self.screen, YELLOW, (vx - WALL_THICK//2, vy, WALL_THICK, h_h), 2)
        # === FIN DEBUG VISUAL ===

        # draw pawns
        for i,p in enumerate(self.game.board.pawns):
            x,y = self.board_to_pixel(p.pos.r, p.pos.c)
            color = BLUE if i==0 else RED
            pygame.draw.circle(self.screen,color,(x+CELL//2,y+CELL//2),CELL//2-6)
        # UI text
        info = f"Mode: {self.selected_mode.upper()} | Turn: {self.players[self.game.turn%2].name}"
        self.screen.blit(FONT.render(info, True, BLACK), (10, self.window_h - 70))
        walls_p1_info = f"Walls left player 1: {self.game.board.pawns[0].walls_left}"
        self.screen.blit(FONT.render(walls_p1_info, True, BLACK), (10, self.window_h - 50))
        walls_p2_info = f"Walls left player 2: {self.game.board.pawns[1].walls_left}"
        self.screen.blit(FONT.render(walls_p2_info, True, BLACK), (10, self.window_h - 30))
        pygame.display.flip()

    def save_history(self):
        self.history.append(self.game.clone())
        if len(self.history) > 50:
            self.history.pop(0)

    def undo(self):
        if self.history:
            self.game = self.history.pop()

    def human_move_action(self, cell_kind,r,c):
        self.save_history()
        ok = False
        if cell_kind=='cell' and self.selected_mode=='move':
            ok = self.game.move_pawn(r,c)
        elif cell_kind=='hslot' and self.selected_mode=='hwall':
            ok = self.game.place_horiz(r,c)
        elif cell_kind=='vslot' and self.selected_mode=='vwall':
            ok = self.game.place_vert(r,c)
        if not ok and self.history: self.history.pop()
        else:
            self.check_winner()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))

    def ai_move_for_player(self, player):
        if self.game.winner is not None: 
            return
        
        t0 = time.time()
        fixed = self.game.turn % 2

        score, mv = minimax(
            self.game,
            player_id=fixed,
            fixed_player_id=fixed,
            depth=player.depth,
            max_player=True,
            use_alphabeta=player.use_alphabeta,
            eval_function=player.eval_fun
        )

        t1 = time.time()
        self.total_time[fixed] += (t1 - t0)

        if mv is None:
            print(f"{player.name}: sin jugadas legales. Paso/empate forzado.")
            # en headless, avanzamos el loop llamando al siguiente si corresponde
            if self.headless and self.running:
                self._maybe_continue_headless()
            else:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))
            return
        
        kind, param = mv
        if kind == 'move': self.game.move_pawn(param[0], param[1])
        elif kind == 'hwall': self.game.place_horiz(param[0], param[1])
        else: self.game.place_vert(param[0], param[1])

        print(f"{player.name} move:", mv, "score:", round(score,2), "time:", round(t1-t0,2))
        self.check_winner()

        if self.headless:
            self._maybe_continue_headless()
        else:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))

    def _maybe_continue_headless(self):
        if not self.running:
            return
        
        # En headless, por construcción, siempre ambos son IA
        current = self.players[self.game.turn % 2]
        self.ai_move_for_player(current)
    
    def check_winner(self):
        if self.game.winner is not None:
            winner_idx = self.game.winner.index  # 0 o 1
            winner_player = self.players[winner_idx].name
            print(f"¡Juego terminado! Ganador: {winner_player}")
            print(f"Tiempo total Player 1: {round(self.total_time[0], 2)}s")
            print(f"Tiempo total Player 2: {round(self.total_time[1], 2)}s")
            self.running = False

    def run(self):
        if self.headless:
            while self.running and self.game.winner is None:
                self.clock.tick(FPS)
                pygame.quit()
            return
        
        while self.running:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: self.running=False
                elif ev.type==pygame.KEYDOWN:
                    if ev.key==pygame.K_h: self.selected_mode='hwall'
                    elif ev.key==pygame.K_v: self.selected_mode='vwall'
                    elif ev.key==pygame.K_m: self.selected_mode='move'
                    elif ev.key==pygame.K_u: self.undo()
                    elif ev.key==pygame.K_ESCAPE: self.running=False
                elif ev.type==pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    hit = self.pixel_to_cell(pos[0],pos[1])
                    current_player = self.players[self.game.turn%2]
                    if hit and current_player.is_human:
                        kind,r,c = hit
                        self.human_move_action(kind,r,c)
                elif ev.type==pygame.USEREVENT+1:
                    current_player = self.players[self.game.turn%2]
                    if not current_player.is_human:
                        self.ai_move_for_player(current_player)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
