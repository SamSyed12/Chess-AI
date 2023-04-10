import sys

import pygame

from game import Game
from minmax import *


class RunChess:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Window_Size)
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.update = True

    def chess_loop(self):

        while True:
            self.game.create_board(self.screen)
            self.game.highlight_previous_move(self.screen)
            self.game.display_moves(self.screen)
            self.game.display_pieces(self.screen)
            self.game.display_square_choice(self.screen)
            self.game.checkmate(self.screen)

            if not self.game.game_over:
                if self.game.next_turn == "white":
                    x, y = pygame.mouse.get_pos()

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            square_row = int(y // Board_Square_Size)
                            square_column = int(x // Board_Square_Size)
                            self.game.set_available_square(square_row, square_column)
                            self.game.display_square_choice(self.screen)

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.game.click_event(event.pos[0], event.pos[1])
                            self.game.create_board(self.screen)
                            self.game.highlight_previous_move(self.screen)
                            self.game.display_moves(self.screen)
                            self.game.display_pieces(self.screen)
                            self.game.display_square_choice(self.screen)
                else:
                    self.game.checkmate(self.screen)
                    make_random_move(self.game.board)
                    self.game.checkmate(self.screen)

                    if self.game.next_turn == "white":
                        self.game.next_turn = "black"
                    else:
                        self.game.next_turn = "white"

                pygame.display.update()


main = RunChess()
main.chess_loop()
