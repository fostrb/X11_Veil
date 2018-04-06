from tools.brushes.brush import Brush
from images.freehand import FreehandImage
from images.glowscribble import GlowScribble


class FreehandBrush(Brush):
    def __init__(self, width=7, color=None):
        super(FreehandBrush, self).__init__()
        self.name = "Freehand"
        self.width = width
        self.color = color
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = FreehandImage(self.width, self.color, [[event.x, event.y]], glow=veil.glow)
            veil.images.append(self.active_stroke)

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        self.active_stroke.points.append((event.x, event.y))
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.active_stroke = None
        veil.queue_draw()
