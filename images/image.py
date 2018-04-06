from random import random as rand
from random import randint


class Image(object):
    def __init__(self):
        self.glowing_lines = []  # width, color

    def draw(self, ctx):
        pass

    def set_glow(self, glow):
        pass

    @staticmethod
    def random_color(alpha=1):
        return rand(), rand(), rand(), alpha

    @staticmethod
    def make_gradient(color, width, steps):
        gradient = []
        r, g, b, a = color

        for step in range(1, steps+1):
            this_width = width*2 - (width * (step/steps))
            this_alpha = step / steps
            gradient.append([this_width, [r, g, b, this_alpha]])
        return gradient

    @staticmethod
    def random_strong_color(alpha):
        c = randint(1, 6)
        if c == 1:
            return 0, 0, 1, alpha
        elif c == 2:
            return 0, 1, 0, alpha
        elif c == 3:
            return 0, 1, 1, alpha
        elif c == 4:
            return 1, 0, 0, alpha
        elif c == 5:
            return 1, 0, 1, alpha
        elif c == 6:
            return 1, 1, 0, alpha
        elif c == 7:
            return 1, 1, 1, alpha