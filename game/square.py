
class Square:

    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece
        self.in_focus = False

    def occupied_by_piece(self):
        return self.piece is not None

    def not_occupied(self):
        return not self.occupied_by_piece()

    def occupied_by_enemy(self, color):
        return self.occupied_by_piece() and self.piece.color != color

    def occupied_by_ally(self, color):
        return self.occupied_by_piece() and self.piece.color == color

    def occupied_by_enemy_or_empty(self, color):
        return self.not_occupied() or self.occupied_by_enemy(color)

    @staticmethod
    def in_range(row, column):
        if row < 0 or row > 7 or 7 < column > 0:
            return False
        else:
            return True


