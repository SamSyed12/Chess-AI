from util import *
from square import Square
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from move import Move
import copy


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(Board_Columns)]
        self.create_squares()
        self.position_pieces("white")
        self.position_pieces("black")
        self.previous_move = None

    def create_squares(self):
        for i in range(Board_Rows):
            for j in range(Board_Columns):
                self.squares[i][j] = Square(i, j)

    def position_pieces(self, color):
        if color == "white":
            pawn_row, other_piece_row = (6, 7)
        else:
            pawn_row, other_piece_row = (1, 0)

        for i in range(Board_Columns):
            self.squares[pawn_row][i].piece = Pawn(color)

        self.squares[other_piece_row][0].piece = Rook(color)
        self.squares[other_piece_row][7].piece = Rook(color)
        self.squares[other_piece_row][1].piece = Knight(color)
        self.squares[other_piece_row][6].piece = Knight(color)
        self.squares[other_piece_row][2].piece = Bishop(color)
        self.squares[other_piece_row][5].piece = Bishop(color)
        self.squares[other_piece_row][3].piece = Queen(color)
        self.squares[other_piece_row][4].piece = King(color)

    def pawn_promotion(self, piece, ending_square):
        if piece.type == "pawn":
            if ending_square.row == 7 or ending_square.row == 0:
                self.squares[ending_square.row][ending_square.column].piece = Queen(piece.color)

    def possible_moves(self, piece, row, column, actual=True):

        def castling():
            if not piece.has_moved:
                if self.squares[row][0].occupied_by_ally(piece.color):
                    if self.squares[row][0].piece.type == "rook":
                        left_rook = self.squares[row][0].piece
                        if not left_rook.has_moved:
                            for col in range(1, 4):
                                if self.squares[row][col].occupied_by_piece():
                                    break

                                if col == 3:
                                    piece.left_rook = left_rook
                                    starting_square_r = Square(row, 0)
                                    ending_square_r = Square(row, 3)
                                    move_rook = Move(starting_square_r, ending_square_r)

                                    starting_square_k = Square(row, column)
                                    ending_square_k = Square(row, 2)
                                    move_king = Move(starting_square_k, ending_square_k)

                                    if actual:
                                        if not self.in_check(left_rook, move_rook):
                                            left_rook.append_move(move_rook)
                                    else:
                                        left_rook.append_move(move_rook)

                                    if actual:
                                        if not self.in_check(piece, move_king):
                                            piece.append_move(move_king)
                                    else:
                                        piece.append_move(move_king)

                if self.squares[row][7].occupied_by_ally(piece.color):
                    if self.squares[row][7].piece.type == "rook":
                        right_rook = self.squares[row][7].piece
                        if not right_rook.has_moved:
                            for col in range(5, 7):
                                if self.squares[row][col].occupied_by_piece():
                                    break

                                if col == 6:
                                    piece.right_rook = right_rook
                                    starting_square_r = Square(row, 7)
                                    ending_square_r = Square(row, 5)
                                    move_rook = Move(starting_square_r, ending_square_r)

                                    starting_square_k = Square(row, column)
                                    ending_square_k = Square(row, 6)
                                    move_king = Move(starting_square_k, ending_square_k)

                                    if actual:
                                        if not self.in_check(right_rook, move_rook):
                                            right_rook.append_move(move_rook)
                                    else:
                                        right_rook.append_move(move_rook)

                                    if actual:
                                        if not self.in_check(piece, move_king):
                                            piece.append_move(move_king)
                                    else:
                                        piece.append_move(move_king)

        def pawn_moves():
            vertical_moves_available = []
            if row == 6 or row == 1:
                vertical_moves_available.append((row + piece.direction, column))
                vertical_moves_available.append((row + 2 * piece.direction, column))
            else:
                vertical_moves_available.append((row + piece.direction, column))

            for move in vertical_moves_available:
                move_row = move[0]
                move_column = move[1]

                if Square.in_range(move_row, move_column):
                    if self.squares[move_row][move_column].not_occupied():
                        starting_square = Square(row, column)
                        ending_piece = self.squares[move_row][move_column].piece
                        ending_square = Square(move_row, move_column, ending_piece)
                        move = Move(starting_square, ending_square)

                        if actual:
                            if not self.in_check(piece, move):
                                piece.append_move(move)
                        else:
                            piece.append_move(move)
                    else:
                        break
                else:
                    break

            diagonal_moves_available = []
            x = row + piece.direction
            diagonal_moves_available.append((row + piece.direction, column - 1))
            diagonal_moves_available.append((x, column + 1))

            for move in diagonal_moves_available:
                move_row = move[0]
                move_column = move[1]
                if Square.in_range(move_row, move_column):
                    if self.squares[move_row][move_column].occupied_by_enemy(piece.color):
                        starting_square = Square(row, column)
                        ending_piece = self.squares[move_row][move_column].piece
                        ending_square = Square(move_row, move_column, ending_piece)
                        move = Move(starting_square, ending_square)

                        if actual:
                            if not self.in_check(piece, move):
                                piece.append_move(move)
                        else:
                            piece.append_move(move)

            en_passant_moves_available = []

            if piece.color == "white":
                accessible_row = 3
            else:
                accessible_row = 4

            en_passant_moves_available.append((accessible_row, column-1))
            en_passant_moves_available.append((accessible_row, column+1))

            for move in en_passant_moves_available:
                move_row = move[0]
                move_column = move[1]
                ending_row = move[0] + piece.direction

                if row == accessible_row:
                    if Square.in_range(move_row, move_column):
                        if self.squares[move_row][move_column].occupied_by_enemy(piece.color):
                            enemy_piece = self.squares[move_row][move_column].piece
                            if enemy_piece.type == "pawn":
                                if enemy_piece.en_passant:
                                    if Square.in_range(ending_row, move_column):
                                        if self.squares[ending_row][move_column].not_occupied():
                                            starting_square = Square(row, column)
                                            ending_square = Square(ending_row, move_column, enemy_piece)
                                            move = Move(starting_square, ending_square)

                                            if actual:
                                                if not self.in_check(piece, move):
                                                    piece.append_move(move)
                                            else:
                                                piece.append_move(move)

        def knight_moves():
            moves_available = [
                (row + 1, column + 2),
                (row + 1, column - 2),
                (row - 1, column + 2),
                (row - 1, column - 2),
                (row + 2, column + 1),
                (row + 2, column - 1),
                (row - 2, column + 1),
                (row - 2, column - 1)
            ]

            for move in moves_available:
                move_row = move[0]
                move_column = move[1]

                if Square.in_range(move_row, move_column):
                    if self.squares[move_row][move_column].occupied_by_enemy_or_empty(piece.color):
                        starting_square = Square(row, column)
                        ending_piece = self.squares[move_row][move_column].piece
                        ending_square = Square(move_row, move_column, ending_piece)
                        move = Move(starting_square, ending_square)

                        if actual:
                            if not self.in_check(piece, move):
                                piece.append_move(move)
                        else:
                            piece.append_move(move)

        def linear_moves(directions):

            for direction in directions:
                row_dir = direction[0]
                column_dir = direction[1]

                possible_row = row + row_dir
                possible_column = column + column_dir

                while 0 <= possible_row < 8 and 0 <= possible_column < 8:
                    if Square.in_range(possible_row, possible_column):
                        if self.squares[possible_row][possible_column].not_occupied():
                            starting_square = Square(row, column)
                            ending_square = Square(possible_row, possible_column)
                            move = Move(starting_square, ending_square)

                            if actual:
                                if not self.in_check(piece, move):
                                    piece.append_move(move)
                            else:
                                piece.append_move(move)

                        elif self.squares[possible_row][possible_column].occupied_by_enemy(piece.color):
                            starting_square = Square(row, column)
                            ending_piece = self.squares[possible_row][possible_column].piece
                            ending_square = Square(possible_row, possible_column, ending_piece)
                            move = Move(starting_square, ending_square)

                            if actual:
                                if not self.in_check(piece, move):
                                    piece.append_move(move)
                                else:
                                    break
                            else:
                                piece.append_move(move)

                            break

                        if self.squares[possible_row][possible_column].occupied_by_ally(piece.color):
                            break
                    else:
                        break

                    possible_row = possible_row + row_dir
                    possible_column = possible_column + column_dir

        def king_moves():
            available_moves = [
                (row + 1, column + 1),
                (row - 1, column - 1),
                (row - 1, column + 1),
                (row + 1, column - 1),
                (row + 1, column),
                (row - 1, column),
                (row, column + 1),
                (row, column - 1),
            ]

            for move in available_moves:
                move_row = move[0]
                move_column = move[1]

                if Square.in_range(move_row, move_column):
                    if self.squares[move_row][move_column].occupied_by_enemy_or_empty(piece.color):
                        starting_square = Square(row, column)
                        ending_square = Square(move_row, move_column)
                        move = Move(starting_square, ending_square)
                        if actual:
                            if not self.in_check(piece, move):
                                piece.append_move(move)
                        else:
                            piece.append_move(move)
            castling()

        if piece.type == "pawn":
            pawn_moves()
        elif piece.type == "rook":
            linear_moves([(-1, 0), (1, 0), (0, -1), (0, 1)])
        elif piece.type == "bishop":
            linear_moves([(1, 1), (-1, -1), (-1, 1), (1, -1)])
        elif piece.type == "knight":
            knight_moves()
        elif piece.type == "queen":
            linear_moves([(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)])
        elif piece.type == "king":
            king_moves()

    def make_move(self, piece, move):
        starting_square = move.starting_square
        ending_square = move.ending_square

        en_passant_square_access = self.squares[ending_square.row][ending_square.column]

        if piece.type == "king":
            if abs(starting_square.column - ending_square.column) == 2:
                direction_indicator = ending_square.column - starting_square.column

                if direction_indicator == -2:
                    rook = piece.left_rook
                    self.make_move(rook, rook.moves[-1])

                elif direction_indicator == 2:
                    rook = piece.right_rook
                    self.make_move(rook, rook.moves[-1])

        if piece.type == "pawn":
            dis_moved = ending_square.column - starting_square.column
            if dis_moved != 0:
                if en_passant_square_access.not_occupied():
                    self.squares[starting_square.row][starting_square.column + dis_moved].piece = None
                    self.squares[ending_square.row][ending_square.column].piece = piece

        self.squares[starting_square.row][starting_square.column].piece = None
        self.squares[ending_square.row][ending_square.column].piece = piece

        self.pawn_promotion(piece, ending_square)

        piece.has_moved = True
        piece.moves = []
        self.previous_move = move
        self.reset_en_passant(piece)

    def reset_en_passant(self, piece):
        for row in range(Board_Rows):
            for column in range(Board_Columns):
                if self.squares[row][column].piece:
                    if self.squares[row][column].piece.type == "pawn":
                        self.squares[row][column].piece.en_passant = False

        if piece.type == "pawn":
            piece.en_passant = True

    def accessible_move(self, piece, _move_):
        is_accessible = False
        x1 = _move_.starting_square.row
        y1 = _move_.starting_square.column
        x2 = _move_.ending_square.row
        y2 = _move_.ending_square.column
        for move in piece.moves:
            if x1 == move.starting_square.row:
                if y1 == move.starting_square.column:
                    if x2 == move.ending_square.row:
                        if y2 == move.ending_square.column:
                            is_accessible = True
        return is_accessible

    def in_check(self, piece, move):
        piece_copy = copy.deepcopy(piece)
        board_copy = copy.deepcopy(self)
        board_copy.make_move(piece_copy, move)

        for i in range(Board_Rows):
            for j in range(Board_Columns):
                if board_copy.squares[i][j].occupied_by_enemy(piece.color):
                    enemy_piece = board_copy.squares[i][j].piece
                    board_copy.possible_moves(enemy_piece, i, j, actual=False)
                    for the_move in enemy_piece.moves:
                        if the_move.ending_square.piece:
                            if the_move.ending_square.piece.type == "king":
                                return True
        return False

    def is_in_checkmate(self, color):
        board_copy = copy.deepcopy(self)

        for i in range(Board_Rows):
            for j in range(Board_Columns):
                if board_copy.squares[i][j].occupied_by_ally(color):
                    ally_piece = board_copy.squares[i][j].piece
                    board_copy.possible_moves(ally_piece, i, j, actual=True)
                    if len(ally_piece.moves) > 0:
                        return False

        return True
