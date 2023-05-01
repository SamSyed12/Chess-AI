from util import *
import math


def evaluation(board, color):
    score = 0

    for i in range(Board_Rows):
        for j in range(Board_Columns):
            square = board.squares[i][j]

            if not square.piece:
                continue

            piece_value = square.piece.value

            if color == "white":

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
                        piece_value += king_bonus_matrix[i][j]

                    for move in square.piece.moves:
                        if move.ending_square.occupied_by_enemy(color):
                            piece_value += (move.ending_square.piece.value * -1)
                else:
                    if square.piece.type == 'pawn':
                        piece_value -= black_pawn_matrix[i][j]

                    elif square.piece.type == 'knight':
                        piece_value -= black_knight_matrix[i][j]

                    elif square.piece.type == 'rook':
                        piece_value -= black_rook_matrix[i][j]

                    elif square.piece.type == 'bishop':
                        piece_value -= black_bishop_matrix[i][j]

                    elif square.piece.type == 'queen':
                        piece_value -= black_queen_matrix[i][j]

                    elif square.piece.type == 'king':
                        piece_value -= black_king_matrix[i][j]

                    for move in square.piece.moves:
                        if move.ending_square.occupied_by_ally(color):
                            piece_value -= (move.ending_square.piece.value * -1)
            else:

                if square.occupied_by_ally(color):

                    if square.piece.type == 'pawn':
                        piece_value += black_pawn_matrix[i][j]

                    elif square.piece.type == 'knight':
                        piece_value += black_knight_matrix[i][j]

                    elif square.piece.type == 'rook':
                        piece_value += black_rook_matrix[i][j]

                    elif square.piece.type == 'bishop':
                        piece_value += black_bishop_matrix[i][j]

                    elif square.piece.type == 'queen':
                        piece_value += black_queen_matrix[i][j]

                    elif square.piece.type == 'king':
                        piece_value += black_king_matrix[i][j]

                    for move in square.piece.moves:
                        if move.ending_square.occupied_by_enemy(color):
                            piece_value += (move.ending_square.piece.value * -1)/3
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
                        piece_value -= king_bonus_matrix[i][j]

                    for move in square.piece.moves:
                        if move.ending_square.occupied_by_ally(color):
                            piece_value -= (move.ending_square.piece.value * -1)/3

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

# def max_val(board, depth, alpha, beta, next_turn):
#     if depth == 0:
#         return evaluation(board, next_turn)
#     best_value = -math.inf
#     possible_moves = board.get_valid_moves(next_turn)
#
#     if len(possible_moves) == 0:
#         return evaluation(board, next_turn)
#
#     for move in possible_moves:
#         piece = move[0]
#         the_move = move[1]
#         board.make_move(piece, the_move)
#         value = min_val(board, depth - 1, alpha, beta, next_turn)
#         best_value = max(best_value, value)
#         alpha = max(alpha, best_value)
#         board.undo_move(piece, the_move)
#         if alpha >= beta:
#             break
#     return best_value
#
#
# def min_val(board, depth, alpha, beta, next_turn):
#     if depth == 0:
#         return evaluation(board, next_turn)
#     best_value = math.inf
#
#     possible_moves = board.get_valid_moves(next_turn)
#
#     if len(possible_moves) == 0:
#         return evaluation(board, next_turn)
#
#     for move in possible_moves:
#         piece = move[0]
#         the_move = move[1]
#         board.make_move(piece, the_move)
#         value = max_val(board, depth - 1, alpha, beta, next_turn)
#         best_value = min(best_value, value)
#         beta = min(beta, best_value)
#         board.undo_move(piece, the_move)
#         if beta <= alpha:
#             break
#     return best_value
#
#
# def minimax(depth, board, next_turn):
#     alpha = -math.inf
#     beta = math.inf
#
#     valid_moves = board.get_valid_moves(next_turn)
#
#     max_value = -math.inf
#     min_value = math.inf
#
#     if len(valid_moves) > 0:
#         best_move = valid_moves[0]
#
#         if next_turn == "white":
#             for move in valid_moves:
#                 piece = move[0]
#                 the_move = move[1]
#                 board.make_move(piece, the_move)
#                 value = max_val(board, depth, alpha, beta, next_turn)
#                 if value > max_value:
#                     max_value = value
#                     best_move = move
#                 board.undo_move(piece, the_move)
#
#         else:
#             for move in valid_moves:
#                 piece = move[0]
#                 the_move = move[1]
#                 board.make_move(piece, the_move)
#                 value = min_val(board, depth, alpha, beta, next_turn)
#                 if value < min_value:
#                     min_value = value
#                     best_move = move
#                 board.undo_move(piece, the_move)
#     else:
#         value = evaluation(board, next_turn)
#         best_move = None
#
#     return value, best_move


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

king_bonus_matrix = [
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
    [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
    [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
    [0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2]
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

black_king_matrix = king_bonus_matrix[::-1]
for i in range(len(black_king_matrix)):
    black_king_matrix[i] = black_king_matrix[i][::-1]

black_king_matrix = [[-1 * element for element in row] for row in black_king_matrix]


