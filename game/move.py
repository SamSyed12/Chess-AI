from square import Square


class Move:

    def __init__(self, starting_square, ending_square):
        self.starting_square = starting_square
        self.ending_square = ending_square

    def __str__(self):
        info = ""
        info += (self.starting_square.row, self.starting_square.column)
        info += (self.ending_square.row, self.ending_square.column)
        return info


