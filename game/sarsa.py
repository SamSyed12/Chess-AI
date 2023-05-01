import random
import numpy as np

from util import *


class Sarsa:
    def __init__(self, epsilon=0.2, alpha=0.7, gamma=0.8, weights=[0.1, 0.32, 0.33, 0.5, 1.5, 1, -0.1, -0.32, -0.33, -0.5, -1.5, -1]):
        self.epsilon = epsilon
        self.prev_state = None
        self.curr_state = None
        self.prev_action = None
        self.curr_action = None
        self.alpha = alpha
        self.gamma = gamma
        self.weights = weights

    def random_move(self, possible_moves):
        if len(possible_moves) == 0:
            return
        else:
            random_num = random.randint(0, len(possible_moves) - 1)
            random_move = possible_moves[random_num]
            return random_move

    def return_move(self, board, next_turn):

        self.curr_state = board
        self.curr_action = self.take_action(board, next_turn)

        if self.prev_state is not None:
            self.update_weights(self.prev_state, self.curr_state, next_turn)

        self.prev_state = self.curr_state
        self.prev_action = self.curr_action

        return self.curr_action

    def take_action(self, board, next_turn):

        possible_moves = board.get_valid_moves(next_turn)

        if np.random.uniform() < self.epsilon:
            return self.random_move(possible_moves)
        else:
            q_values = {}
            for move in possible_moves:
                piece = move[0]
                the_move = move[1]
                board.make_move(piece, the_move)
                q_values[move] = np.dot(self.weights, self.feature_vector(board, next_turn))
                board.undo_move(piece, the_move)

            white_value = -99999999999
            black_value = 99999999999

            if next_turn == "white":
                for value in q_values:

                    if q_values[value] > white_value:
                        white_value = q_values[value]

                key_list = list(q_values.keys())
                val_list = list(q_values.values())

                position = val_list.index(white_value)

                return key_list[position]

            else:
                for value in q_values:

                    if q_values[value] < black_value:
                        black_value = q_values[value]

                key_list = list(q_values.keys())
                val_list = list(q_values.values())

                position = val_list.index(black_value)

                return key_list[position]

    def update_weights(self, previous_state, new_state, next_turn):

        updated_weights = self.alpha * (self.gamma * (self.weights * self.feature_vector(new_state, next_turn)) - (self.weights * self.feature_vector(previous_state, next_turn)) * self.feature_vector(previous_state, next_turn))

        for i, weight in enumerate(self.weights):
            self.weights[i] = weight + updated_weights[i]
            if self.weights[i] > 5:
                self.weights[i] = 3
            elif self.weights[i] < -5:
                self.weights[i] = -3

    def update_weights_reward(self, previous_state, next_state, reward, next_turn):

        new_weights = self.alpha * (reward + self.gamma * (self.weights * self.feature_vector(next_state, next_turn)) - (self.weights * self.feature_vector(previous_state, next_turn)) * self.feature_vector(previous_state, next_turn))

        for i, weight in enumerate(self.weights):
            self.weights[i] = weight + new_weights[i]
            if self.weights[i] > 5:
                self.weights[i] = 3
            elif self.weights[i] < -5:
                self.weights[i] = -3

    def feature_vector(self, board, color):

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
            [-0.20, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.20],
            [-0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.10],
            [-0.10, 0.00, 0.05, 0.10, 0.10, 0.05, 0.00, -0.10],
            [-0.10, 0.05, 0.05, 0.10, 0.10, 0.05, 0.05, -0.10],
            [-0.10, 0.00, 0.10, 0.10, 0.10, 0.10, 0.00, -0.10],
            [-0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, -0.10],
            [-0.10, 0.05, 0.00, 0.00, 0.00, 0.00, 0.05, -0.10],
            [-0.20, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.20]
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

        feature_vector = np.zeros(12)

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
                            feature_vector[0] += piece_value

                        elif square.piece.type == 'knight':
                            piece_value += knight_bonus_matrix[i][j]
                            feature_vector[1] += piece_value

                        elif square.piece.type == 'rook':
                            piece_value += rook_bonus_matrix[i][j]
                            feature_vector[2] += piece_value

                        elif square.piece.type == 'bishop':
                            piece_value += bishop_bonus_matrix[i][j]
                            feature_vector[3] += piece_value

                        elif square.piece.type == 'queen':
                            piece_value += queen_bonus_matrix[i][j]
                            feature_vector[4] += piece_value

                        elif square.piece.type == 'king':
                            piece_value += king_bonus_matrix[i][j]
                            feature_vector[5] += piece_value

                    else:
                        if square.piece.type == 'pawn':
                            piece_value -= black_pawn_matrix[i][j]
                            feature_vector[6] -= piece_value

                        elif square.piece.type == 'knight':
                            piece_value -= black_knight_matrix[i][j]
                            feature_vector[7] -= piece_value

                        elif square.piece.type == 'rook':
                            piece_value -= black_rook_matrix[i][j]
                            feature_vector[8] -= piece_value

                        elif square.piece.type == 'bishop':
                            piece_value -= black_bishop_matrix[i][j]
                            feature_vector[9] -= piece_value

                        elif square.piece.type == 'queen':
                            piece_value -= black_queen_matrix[i][j]
                            feature_vector[10] -= piece_value

                        elif square.piece.type == 'king':
                            piece_value -= black_king_matrix[i][j]
                            feature_vector[11] -= piece_value

                else:
                    if square.occupied_by_ally(color):

                        if square.piece.type == 'pawn':
                            piece_value += black_pawn_matrix[i][j]
                            feature_vector[0] += piece_value

                        elif square.piece.type == 'knight':
                            piece_value += black_knight_matrix[i][j]
                            feature_vector[1] += piece_value

                        elif square.piece.type == 'rook':
                            piece_value += black_rook_matrix[i][j]
                            feature_vector[2] += piece_value

                        elif square.piece.type == 'bishop':
                            piece_value += black_bishop_matrix[i][j]
                            feature_vector[3] += piece_value

                        elif square.piece.type == 'queen':
                            piece_value += black_queen_matrix[i][j]
                            feature_vector[4] += piece_value

                        elif square.piece.type == 'king':
                            piece_value += black_king_matrix[i][j]
                            feature_vector[5] += piece_value

                    else:
                        if square.piece.type == 'pawn':
                            piece_value -= pawn_bonus_matrix[i][j]
                            feature_vector[6] -= piece_value

                        elif square.piece.type == 'knight':
                            piece_value -= knight_bonus_matrix[i][j]
                            feature_vector[7] -= piece_value

                        elif square.piece.type == 'rook':
                            piece_value -= rook_bonus_matrix[i][j]
                            feature_vector[8] -= piece_value

                        elif square.piece.type == 'bishop':
                            piece_value -= bishop_bonus_matrix[i][j]
                            feature_vector[9] -= piece_value

                        elif square.piece.type == 'queen':
                            piece_value -= queen_bonus_matrix[i][j]
                            feature_vector[10] -= piece_value

                        elif square.piece.type == 'king':
                            piece_value -= king_bonus_matrix[i][j]
                            feature_vector[11] -= piece_value

        return feature_vector

    def checkmate(self, board, next_turn):

        reward = self.alpha * (board.return_reward(next_turn))
        self.update_weights_reward(self.prev_state, self.curr_state, reward, next_turn)
