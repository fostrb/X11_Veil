import cairo
from tools.brushes.brush import Brush
from images.rectangle import RectangleImage


class FilledRectangleBrush(Brush):
    def __init__(self, edge_width=2, edge_color=None, fill_color=None):
        super(FilledRectangleBrush, self).__init__()
        self.name = "Filled Rectangle"
        self.edge_width = edge_width
        self.o_edge_color = edge_color
        self.o_fill_color = fill_color
        self.images = []
        self.active_stroke = None

    def mouse_move(self, veil, event):
        self.active_stroke.x_current = event.x
        self.active_stroke.y_current = event.y
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.finish(veil)
        veil.queue_draw()

    def mouse_secondary(self, veil, event):
        pass

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = RectangleImage(self.edge_width, self.o_edge_color, self.o_fill_color, event.x, event.y, glow=veil.glow)
            #self.images.append(self.active_stroke)
            veil.images.append(self.active_stroke)
        veil.queue_draw()

    def draw(self, ctx):
        for image in self.images:
            image.draw(ctx)

    def finish(self, veil):
        self.active_stroke = None