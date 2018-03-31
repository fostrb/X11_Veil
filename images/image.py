from random import random as rand


class Image(object):
    def __init__(self):
        pass

    def draw(self, ctx):
        pass

    @staticmethod
    def random_color(alpha=1):
        return rand(), rand(), rand(), alpha