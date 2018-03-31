from tools.brushes.brush import Brush
from images.freehand import FreehandImage


class FreehandBrush(Brush):
    def __init__(self, width=8, color=None):
        super(FreehandBrush, self).__init__()
        self.name = "Freehand"
        self.width = width
        self.color = color
        self.images = []
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = FreehandImage(self.width, self.color, [[event.x, event.y]])
            #self.images.append(self.active_stroke)
            veil.images.append(self.active_stroke)

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        self.active_stroke.points.append((event.x, event.y))
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.active_stroke = None
        veil.queue_draw()

    def draw(self, ctx):
        for image in self.images:
            image.draw(ctx)

    def undo(self):
        if len(self.images) > 0:
            self.images.pop()