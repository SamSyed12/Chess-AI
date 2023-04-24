import random

from util import *
import math


def make_random_move(board):
    possible_moves = []
    for i in range(Board_Rows):
        for j in range(Board_Columns):
            if board.squares[i][j].occupied_by_ally("black"):
                piece = board.squares[i][j].piece
                piece.moves = []
                board.possible_moves(piece, i, j)

                for move in piece.moves:
                    possible_moves.append((piece, move))

    if len(possible_moves) == 0:
        return
    else:
        random_num = random.randint(0, len(possible_moves) - 1)
        random_move = possible_moves[random_num]
        piece = random_move[0]
        move = random_move[1]
        board.make_move(piece, move)


def evaluation(board, color):
    score = 0

    for i in range(Board_Rows):
        for j in range(Board_Columns):
            square = board.squares[i][j]

            if not square.piece:
                continue

            piece_value = square.piece.value

            if square.occupied_by_ally(color):
                if square.piece.type == 'pawn':
                    piece_value += pawn_bonus_matrix[i][j]

                elif square.piece.type == 'knight':
                    piece_value += knight_bonus_matrix[i][j]

                elif square.piece.type == 'rook':
                    piece_value += rook_bonus_matrix[i][j]

                elif square.piece.type == 'bishop':
                    piece_value += bishop_bonus_matrix[i][j]

                elif square.piece.type == 'queen':
                    piece_value += queen_bonus_matrix[i][j]

                elif square.piece.type == 'king':
                    piece_value += king_bonus_matrix_mid_game[i][j]
            else:
                if square.piece.type == 'pawn':
                    piece_value -= pawn_bonus_matrix[i][j]

                elif square.piece.type == 'knight':
                    piece_value -= knight_bonus_matrix[i][j]

                elif square.piece.type == 'rook':
                    piece_value -= rook_bonus_matrix[i][j]

                elif square.piece.type == 'bishop':
                    piece_value -= bishop_bonus_matrix[i][j]

                elif square.piece.type == 'queen':
                    piece_value -= queen_bonus_matrix[i][j]

                elif square.piece.type == 'king':
                    piece_value -= king_bonus_matrix_mid_game[i][j]

            score += piece_value

    return score


def minimax(depth, board, next_turn, alpha, beta):
    if depth == 0:
        return evaluation(board, next_turn), None

    valid_moves = board.get_valid_moves(next_turn)
    if len(valid_moves) == 0:
        return evaluation(board, next_turn), None

    if next_turn == "white":
        value = -math.inf
        best_move = None
        for move in valid_moves:
            piece = move[0]
            the_move = move[1]
            board.make_move(piece, the_move)
            new_value, _ = minimax(depth - 1, board, "black", alpha, beta)
            board.undo_move(piece, the_move)
            if new_value > value:
                value = new_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break

    else:
        value = math.inf
        best_move = None
        for move in valid_moves:
            piece = move[0]
            the_move = move[1]
            board.make_move(piece, the_move)
            new_value, _ = minimax(depth - 1, board, "white", alpha, beta)
            board.undo_move(piece, the_move)
            if new_value < value:
                value = new_value
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break

    return value, best_move

pawn_bonus_matrix = [
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50],
    [0.10, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.10],
    [0.05, 0.05, 0.10, 0.25, 0.25, 0.10, 0.05, 0.05],
    [0.00, 0.00, 0.00, 0.20, 0.20, 0.00, 0.00, 0.00],
    [0.05, -0.05, -0.10, 0.00, 0.00, -0.10, -0.05, 0.05],
    [0.05, 0.10, 0.10, -0.20, -0.20, 0.10, 0.10, 0.05],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
]

knight_bonus_matrix = [
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
    [-0.4, -0.2, 0.0, 0.0, 0.0, 0.0, -0.2, -0.4],
    [-0.3, 0.0, 0.1, 0.15, 0.15, 0.1, 0.0, -0.3],
    [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
    [-0.3, 0.0, 0.15, 0.2, 0.2, 0.15, 0.0, -0.3],
    [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
    [-0.4, -0.2, 0.0, 0.05, 0.05, 0.0, -0.2, -0.4],
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
]

bishop_bonus_matrix = [
    [-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20],
    [-0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,-0.10],
    [-0.10, 0.00, 0.05, 0.10, 0.10, 0.05, 0.00,-0.10],
    [-0.10, 0.05, 0.05, 0.10, 0.10, 0.05, 0.05,-0.10],
    [-0.10, 0.00, 0.10, 0.10, 0.10, 0.10, 0.00,-0.10],
    [-0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,-0.10],
    [-0.10, 0.05, 0.00, 0.00, 0.00, 0.00, 0.05,-0.10],
    [-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20]
]

rook_bonus_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
    [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
    [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
    [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
    [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
    [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
    [0, 0, 0, 0.05, 0.05, 0, 0, 0]
]

queen_bonus_matrix = [
    [-0.20, -0.10, -0.10, -0.05, -0.05, -0.10, -0.10, -0.20],
    [-0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.10],
    [-0.10, 0.00, 0.05, 0.05, 0.05, 0.05, 0.00, -0.10],
    [-0.05, 0.00, 0.05, 0.05, 0.05, 0.05, 0.00, -0.05],
    [0.00, 0.00, 0.05, 0.05, 0.05, 0.05, 0.00, -0.05],
    [-0.10, 0.05, 0.05, 0.05, 0.05, 0.05, 0.00, -0.10],
    [-0.10, 0.00, 0.05, 0.00, 0.00, 0.00, 0.00, -0.10],
    [-0.20, -0.10, -0.10, -0.05, -0.05, -0.10, -0.10, -0.20]
]

king_bonus_matrix_mid_game = [
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
    [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
    [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
    [0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2]
]

king_bonus_matrix_end_game = [
    [-0.5, -0.4, -0.3, -0.2, -0.2, -0.3, -0.4, -0.5],
    [-0.3, -0.2, -0.1, 0.0, 0.0, -0.1, -0.2, -0.3],
    [-0.3, -0.1, 0.2, 0.3, 0.3, 0.2, -0.1, -0.3],
    [-0.3, -0.1, 0.3, 0.4, 0.4, 0.3, -0.1, -0.3],
    [-0.3, -0.1, 0.3, 0.4, 0.4, 0.3, -0.1, -0.3],
    [-0.3, -0.1, 0.2, 0.3, 0.3, 0.2, -0.1, -0.3],
    [-0.3, -0.3, 0.0, 0.0, 0.0, 0.0, -0.3, -0.3],
    [-0.5, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.5],
]


black_pawn_matrix = pawn_bonus_matrix[::-1]
for i in range(len(black_pawn_matrix)):
    black_pawn_matrix[i] = black_pawn_matrix[i][::-1]

black_pawn_matrix = [[-1 * element for element in row] for row in black_pawn_matrix]

black_knight_matrix = knight_bonus_matrix[::-1]
for i in range(len(black_knight_matrix)):
    black_knight_matrix[i] = black_knight_matrix[i][::-1]

black_knight_matrix = [[-1 * element for element in row] for row in black_knight_matrix]

black_bishop_matrix = bishop_bonus_matrix[::-1]
for i in range(len(black_bishop_matrix)):
    black_bishop_matrix[i] = black_bishop_matrix[i][::-1]

black_bishop_matrix = [[-1 * element for element in row] for row in black_bishop_matrix]

black_rook_matrix = rook_bonus_matrix[::-1]
for i in range(len(black_rook_matrix)):
    black_rook_matrix[i] = black_rook_matrix[i][::-1]

black_rook_matrix = [[-1 * element for element in row] for row in black_rook_matrix]

black_queen_matrix = queen_bonus_matrix[::-1]
for i in range(len(black_queen_matrix)):
    black_queen_matrix[i] = black_queen_matrix[i][::-1]

black_queen_matrix = [[-1 * element for element in row] for row in black_queen_matrix]

black_king_matrix_mid_game = king_bonus_matrix_mid_game[::-1]
for i in range(len(black_king_matrix_mid_game)):
    black_king_matrix_mid_game[i] = black_king_matrix_mid_game[i][::-1]

black_king_matrix_mid_game = [[-1 * element for element in row] for row in black_king_matrix_mid_game]

black_king_matrix_end_game = king_bonus_matrix_end_game[::-1]
for i in range(len(black_king_matrix_mid_game)):
    black_king_matrix_end_game[i] = black_king_matrix_end_game[i][::-1]

black_king_matrix_end_game = [[-1 * element for element in row] for row in black_king_matrix_end_game]
