import random

from util import *


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
        random_num = random.randint(0, len(possible_moves)-1)
        random_move = possible_moves[random_num]
        piece = random_move[0]
        move = random_move[1]
        board.make_move(piece, move)


def minmax(depth, board, next_turn):
    if depth == 0:  # If we have reached the maximum search depth
        return evaluation(board, next_turn)  # Evaluate the current board state

    valid_moves = get_valid_moves(board, next_turn)  # Get all valid moves for the current player
    if not valid_moves:  # If there are no valid moves, the game is over
        return evaluation(board, next_turn)  # Evaluate the final board state

    if next_turn == "white":  # If it's the maximizing player's turn
        best_value = float("-inf")
        for move in valid_moves:
            new_board = make_move(board, move)  # Make a new board with the move applied
            value = minmax(depth - 1, new_board, False)
            best_value = max(best_value, value)
        return best_value

    else:  # If it's the minimizing player's turn
        best_value = float("inf")
        for move in valid_moves:
            new_board = make_move(board, move)  # Make a new board with the move applied
            value = minmax(depth - 1, new_board, True, evaluate_func, get_valid_moves_func)
            best_value = min(best_value, value)
        return best_value


def evaluation(board, color):
    score = 0
    for i in range(Board_Rows):
        for j in range(Board_Columns):
            if board[i][j].occupied_by_ally(color):
                piece = board.squares[i][j].piece
                score += piece.value
    return score


def get_valid_moves(board, color):
    possible_moves = []
    for i in range(Board_Rows):
        for j in range(Board_Columns):
            if board.squares[i][j].occupied_by_ally(color):
                piece = board.squares[i][j].piece
                piece.moves = []
                board.possible_moves(piece, i, j)

                for move in piece.moves:
                    possible_moves.append((piece, move))

    return possible_moves

