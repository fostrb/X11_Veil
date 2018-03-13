import cairo
from tools.brushes import Brush


class LineBrush(Brush):
    def __init__(self, event, width=8, color=None):
        super(LineBrush, self).__init__()
        self.width = width
        if color:
            self.color = color
        else:
            self.color = self.random_color_transparent(.5)

        self.x_origin = event.x
        self.y_origin = event.y
        self.x_end = event.x
        self.y_end = event.y

    def mouse_secondary(self, veil, event):
        self.cancel(veil)

    def mouse_move(self, veil, event):
        self.x_end = event.x
        self.y_end = event.y
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.finish(veil)
        veil.queue_draw()

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color)
        ctx.move_to(self.x_origin, self.y_origin)
        ctx.line_to(self.x_end, self.y_end)
        ctx.stroke()
