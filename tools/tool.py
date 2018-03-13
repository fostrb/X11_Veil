import random


class Tool:
    def __init__(self, *args, sensitivity=0):
        self.capturing_movement = False
        self.name = 'AbstractToolClass'

    def mouse_primary(self, veil, event):
        pass

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        pass

    def mouse_release(self, veil, event):
        pass
