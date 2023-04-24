import math
from piece import Piece


class King(Piece):

    def __init__(self, color):
        self.right_rook = None
        self.left_rook = None
        super().__init__("king", color, 200)


