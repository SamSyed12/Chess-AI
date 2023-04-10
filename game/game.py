import pygame

from util import *
from board import Board
from move import Move


class Game:

    def __init__(self):
        self.board = Board()
        self.available_square = None
        self.next_turn = "white"
        self.chosen_piece = None
        self.display_the_moves = False
        self.previous_square = None
        self.next_square = None
        self.square_for_checkmate = None
        self.game_over = False

    def create_board(self, surface):
        for i in range(Board_Rows):
            for j in range(Board_Columns):
                if (i + j) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (50, 50, 50)

                square = (i * Board_Square_Size, j * Board_Square_Size, Board_Square_Size, Board_Square_Size)

                pygame.draw.rect(surface, color, square)

    def display_pieces(self, surface):
        for i in range(Board_Rows):
            for j in range(Board_Columns):
                if self.board.squares[i][j].occupied_by_piece():
                    piece = self.board.squares[i][j].piece
                    image = pygame.image.load(piece.image)
                    img_center = j * Board_Square_Size + Board_Square_Size // 2, i * Board_Square_Size + Board_Square_Size // 2
                    piece.image_rect = image.get_rect(center=img_center)
                    surface.blit(image, piece.image_rect)

    def display_moves(self, surface):
        if self.display_the_moves:
            for move in self.chosen_piece.moves:

                if (move.ending_square.row + move.ending_square.column) % 2 == 0:
                    color = (189, 112, 255)
                else:
                    color = (203, 142, 255)

                square = (move.ending_square.column * Board_Square_Size, move.ending_square.row * Board_Square_Size,
                          Board_Square_Size, Board_Square_Size)
                pygame.draw.rect(surface, color, square)

    def get_relevant_square(self, x, y):
        square_row = int(y // Board_Square_Size)
        square_column = int(x // Board_Square_Size)
        return self.board.squares[square_row][square_column]

    def click_event(self, x, y):

        relevant_square = self.get_relevant_square(x, y)
        self.square_for_checkmate = relevant_square

        if self.chosen_piece is None:
            if relevant_square.piece is not None:
                if relevant_square.piece.color == self.next_turn:
                    self.chosen_piece = relevant_square.piece
                    self.board.possible_moves(self.chosen_piece, relevant_square.row, relevant_square.column)
                    self.display_the_moves = True

                    self.previous_square = relevant_square
                    self.next_square = None

        elif self.chosen_piece and relevant_square.occupied_by_ally(self.chosen_piece.color):
            self.chosen_piece.moves = []
            self.chosen_piece = relevant_square.piece
            self.board.possible_moves(self.chosen_piece, relevant_square.row, relevant_square.column)
            self.display_the_moves = True
            self.previous_square = relevant_square
            self.next_square = None

        elif self.chosen_piece and relevant_square.occupied_by_enemy_or_empty(self.chosen_piece.color):
            self.next_square = relevant_square
            move = Move(self.previous_square, self.next_square)
            if self.board.accessible_move(self.chosen_piece, move):
                self.board.make_move(self.chosen_piece, move)
                self.post_move_reset()

    def post_move_reset(self):
        self.chosen_piece = None
        self.display_the_moves = False
        self.previous_square = None
        self.next_square = None

        if self.next_turn == "white":
            self.next_turn = "black"
        else:
            self.next_turn = "white"


    def highlight_previous_move(self, surface):
        if self.board.previous_move:
            starting_square = self.board.previous_move.starting_square
            ending_square = self.board.previous_move.ending_square

            for square in [starting_square, ending_square]:
                if (square.row + square.column) % 2 == 0:
                    color = (255, 255, 224)
                else:
                    color = (255, 255, 204)

                rect = (square.column * Board_Square_Size, square.row * Board_Square_Size,
                        Board_Square_Size, Board_Square_Size)
                pygame.draw.rect(surface, color, rect)

    def display_square_choice(self, surface):
        if self.available_square:
            color = (255, 0, 0)
            rect = (self.available_square.column * Board_Square_Size, self.available_square.row * Board_Square_Size,
                    Board_Square_Size, Board_Square_Size)
            pygame.draw.rect(surface, color, rect, 5)

    def set_available_square(self, row, column):
        self.available_square = self.board.squares[row][column]

    def checkmate(self, surface):
        if self.board.is_in_checkmate(self.next_turn):
            font = pygame.font.Font(None, 100)
            text_surface = font.render(self.next_turn + "loses!", True, (255, 0, 0))
            text_width, text_height = text_surface.get_size()
            text_x = (Screen_Width - text_width) // 2
            text_y = (Screen_Height - text_height) // 2
            surface.blit(text_surface, (text_x, text_y))
            self.game_over = True
