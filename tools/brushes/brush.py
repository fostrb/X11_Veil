import random
from tools.tool import Tool


class Brush(Tool):
    def __init__(self, *args, sensitivity=0):
        super(Brush, self).__init__()
        self.capturing_movement = False
        self.name = 'AbstractBrushClass'

        self.POINTS_DRAGGABLE = False
        self.TRANSLATEABLE = False

    def mouse_primary(self, veil, event):
        pass

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        pass

    def mouse_release(self, veil, event):
        pass

    def draw(self, ctx):
        pass

    @staticmethod
    def cancel(veil):
        veil.active_tool = None
        veil.queue_draw()

    def finish(self, veil):
        veil.brushes.append(self)
        veil.active_tool = None
        veil.queue_draw()

    @staticmethod
    def random_color_transparent(alpha=.5):
        return random.random(), random.random(), random.random(), alpha

    @property
    def random_color_opaque(self):
        return random.random(), random.random(), random.random(), 1