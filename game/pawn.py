from piece import Piece


class Pawn(Piece):

    def __init__(self, color):
        super().__init__("pawn", color, 1.0)
        if color == "white":
            self.direction = -1
        else:
            self.direction = 1
        self.en_passant = False

