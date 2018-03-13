import cairo
from utils.brushes.brush import Brush


class FilledRectangleBrush(Brush):
    def __init__(self, event, edge_width=2, edge_color=None, fill_color=None):
        super(FilledRectangleBrush, self).__init__()
        self.edge_width = edge_width
        if edge_color:
            self.edge_color = edge_color
        else:
            self.edge_color = self.random_color_transparent(.7)
        if fill_color:
            self.fill_color = fill_color
        else:
            self.fill_color = self.random_color_transparent(.2)
        self.x_begin = event.x
        self.y_begin = event.y
        self.x_end = event.x
        self.y_end = event.y

    def mouse_move(self, veil, event):
        self.x_end = event.x
        self.y_end = event.y
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.finish(veil)
        veil.queue_draw()

    def draw(self, ctx):
        size_x = self.x_end - self.x_begin
        size_y = self.y_end - self.y_begin
        ctx.set_line_width(self.edge_width)

        ctx.set_source_rgba(*self.fill_color)
        ctx.rectangle(self.x_begin, self.y_begin, size_x, size_y)
        ctx.fill()

        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.rectangle(self.x_begin, self.y_begin, size_x, size_y)
        ctx.stroke()

        ctx.set_operator(cairo.OPERATOR_OVER)

        ctx.set_source_rgba(*self.edge_color)
        ctx.rectangle(self.x_begin, self.y_begin, size_x, size_y)
        ctx.stroke()
