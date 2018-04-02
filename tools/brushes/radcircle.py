from tools.brushes import Brush
from images.radcircle import RadCircle


class CircleBrush(Brush):
    def __init__(self, edge_width=3, edge_color=None, fill_color=None):
        super(CircleBrush, self).__init__()
        self.name = "CircleBrush"
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = RadCircle(event, self.edge_width, self.edge_color, self.fill_color)
            veil.images.append(self.active_stroke)

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        if self.active_stroke:
            self.active_stroke.x_current = int(event.x)
            self.active_stroke.y_current = int(event.y)
            veil.queue_draw()

    def mouse_release(self, veil, event):
        if self.active_stroke:
            self.active_stroke.complete = True
            self.active_stroke = None
        veil.queue_draw()