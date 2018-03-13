import cairo
from utils.brushes.brush import Brush

class FreehandBrush(Brush):
    def __init__(self, event, width=8, color=None):
        super(FreehandBrush, self).__init__()
        self.width = width
        if color:
            self.color = color
        else:
            self.color = self.random_color_transparent(.5)
        self.stroke = []
        self.stroke.append((event.x, event.y))

    def mouse_move(self, veil, event):
        self.stroke.append((event.x, event.y))
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.finish(veil)
        veil.queue_draw()

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color)
        ctx.set_line_width(self.width)
        ctx.set_line_cap(1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.new_path()
        for x, y in self.stroke:
            ctx.line_to(x, y)
        ctx.stroke()