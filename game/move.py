from square import Square


class Move:

    def __init__(self, starting_square, ending_square, captured_piece=None):
        self.starting_square = starting_square
        self.ending_square = ending_square
        self.captured_piece = captured_piece

    def __str__(self):
        info = ""
        info += (self.starting_square.row, self.starting_square.column)
        info += (self.ending_square.row, self.ending_square.column)
        return info


