import os


class Piece:

    def __init__(self, type, color, value, image=None, image_rect=None):
        self.type = type
        self.color = color
        if color == "white":
            self.value = value * 1
        else:
            self.value = value * -1
        self.image = image
        self.set_image()
        self.image_rect = image_rect
        self.moves = []
        self.has_moved = False

    def set_image(self):
        self.image = os.path.join(f'images/{self.color}_{self.type}.png')

    def append_move(self, move):
        self.moves.append(move)


