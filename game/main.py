import sys
import pygame

from game import Game
from minmax import *
from q_player import QPlayer
from sarsa import Sarsa


class RunChess:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Window_Size)
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.player_white = True
        self.player_black = True
        self.minmax_white = False
        self.minmax_black = False
        self.sarsa_white = False
        self.sarsa_black = False
        self.q_learning_white = False
        self.q_learning_black = False
        self.sarsa = Sarsa()
        self.q_player = QPlayer()

    def chess_loop(self):

        while True:
            self.game.create_board(self.screen)
            self.game.highlight_previous_move(self.screen)
            self.game.display_moves(self.screen)
            self.game.display_pieces(self.screen)
            self.game.display_square_choice(self.screen)
            self.game.checkmate(self.screen)

            if not self.game.game_over:
                x, y = pygame.mouse.get_pos()

                if self.game.board.next_turn == "white":

                    pygame.display.update()

                    if self.minmax_white:
                        value, best_move = minimax(2, self.game.board, "white", alpha=-math.inf, beta=math.inf)
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])
                    if self.sarsa_white:
                        best_move = self.sarsa.return_move(self.game.board, "white")
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])
                    if self.q_learning_white:
                        best_move = self.q_player.return_move(self.game.board, "white")
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])

                    pygame.display.update()

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            if self.player_white:
                                square_row = int(y // Board_Square_Size)
                                square_column = int(x // Board_Square_Size)
                                self.game.set_available_square(square_row, square_column)
                                self.game.display_square_choice(self.screen)

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if self.player_white:
                                self.game.click_event(event.pos[0], event.pos[1])
                                self.game.create_board(self.screen)
                                self.game.highlight_previous_move(self.screen)
                                self.game.display_moves(self.screen)
                                self.game.display_pieces(self.screen)
                                self.game.display_square_choice(self.screen)

                    self.game.create_board(self.screen)
                    self.game.highlight_previous_move(self.screen)
                    self.game.display_pieces(self.screen)
                    self.game.checkmate(self.screen)

                elif self.game.board.next_turn == "black":

                    pygame.display.update()

                    if self.minmax_black:
                        value, best_move = minimax(2, self.game.board, "black", alpha=-math.inf, beta=math.inf)
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])
                    if self.sarsa_black:
                        best_move = self.sarsa.return_move(self.game.board, "black")
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])
                    if self.q_learning_black:
                        best_move = self.q_player.return_move(self.game.board, "black")
                        if best_move is not None:
                            self.game.board.make_move(best_move[0], best_move[1])

                    pygame.display.update()

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            if self.player_black:
                                square_row = int(y // Board_Square_Size)
                                square_column = int(x // Board_Square_Size)
                                self.game.set_available_square(square_row, square_column)
                                self.game.display_square_choice(self.screen)

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if self.player_black:
                                self.game.click_event(event.pos[0], event.pos[1])
                                self.game.create_board(self.screen)
                                self.game.highlight_previous_move(self.screen)
                                self.game.display_moves(self.screen)
                                self.game.display_pieces(self.screen)
                                self.game.display_square_choice(self.screen)

                    self.game.create_board(self.screen)
                    self.game.highlight_previous_move(self.screen)
                    self.game.display_pieces(self.screen)
                    self.game.checkmate(self.screen)
            else:
                self.game.checkmate(self.screen)

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()


main = RunChess()
main.chess_loop()
