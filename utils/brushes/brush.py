import random


class Brush:
    def __init__(self, *args):
        pass

    def mouse_primary(self, veil, event):
        pass

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        pass

    def draw(self, ctx):
        pass

    def finish(self, veil):
        veil.brushes.append(self)

    @staticmethod
    def random_color_transparent(alpha):
        return random.random(), random.random(), random.random(), alpha

    @property
    def random_color_opaque(self):
        return random.random(), random.random(), random.random(), 1
