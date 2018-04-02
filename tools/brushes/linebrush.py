from tools.brushes import Brush
import cairo
from images.line import LineImage


class LineBrush(Brush):
    def __init__(self, width=8, color=None):
        super(LineBrush, self).__init__()
        self.name = "Line"
        self.o_color = color
        self.width = width
        self.color = color
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = LineImage(self.color, self.width, event.x, event.y, event.x, event.y)
            veil.images.append(self.active_stroke)

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        self.active_stroke.x_end = event.x
        self.active_stroke.y_end = event.y
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.active_stroke = None
        veil.queue_draw()