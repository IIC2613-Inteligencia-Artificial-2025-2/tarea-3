import pygame
from player import HumanPlayer, MinimaxPlayer
from ui import UI
from score import evaluate, chat_gpt_eval
from board import BOARD_SIZE

def main(board_size=BOARD_SIZE):
    # Cambia aquí la combinación de jugadores:
    player1 = HumanPlayer("Player 1")
    player2 = HumanPlayer("Player 2")

    # player1 = HumanPlayer("Player 1")
    # player2 = MinimaxPlayer("AI", depth=3, eval_fun=evaluate, use_alphabeta=False)

    # player1 = MinimaxPlayer("AI 1", depth=3, eval_fun=evaluate, use_alphabeta=True)
    # player2 = MinimaxPlayer("AI 2", depth=2, eval_fun=chat_gpt_eval, use_alphabeta=True)

    # headless = False si se muestra la UI siemprew
    # headless = True se oculta la ui solo si ambos jugadores son AI
    ui = UI(player1, player2, board_size=board_size, headless=False)
    ui.run()

if __name__ == "__main__":
    main(board_size=9)
