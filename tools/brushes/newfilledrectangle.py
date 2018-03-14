import cairo
from tools.brushes.brush import Brush


class RectangleImage():
    def __init__(self, edge_width, edge_color, fill_color, x, y):
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.x_origin = x
        self.y_origin = y

        self.x_current = x
        self.y_current = y

class NewFilledRectangleBrush(Brush):
    def __init__(self, edge_width=2, edge_color=None, fill_color=None):
        super(NewFilledRectangleBrush, self).__init__()
        self.edge_width = edge_width
        self.o_edge_color = edge_color
        self.o_fill_color = fill_color
        self.strokes = []
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
            self.active_stroke = RectangleImage(self.edge_width, self.o_edge_color, self.o_fill_color, event.x, event.y)
            self.strokes.append(self.active_stroke)
        if not self.o_edge_color:
            self.active_stroke.edge_color = self.random_color_transparent(.7)
        if not self.o_fill_color:
            self.active_stroke.fill_color = self.random_color_transparent(.2)
        veil.queue_draw()

    def draw_rect(self, ctx, rect_container):
        size_x = rect_container.x_current - rect_container.x_origin
        size_y = rect_container.y_current - rect_container.y_origin
        ctx.set_line_width(rect_container.edge_width)

        ctx.set_source_rgba(*rect_container.fill_color)
        ctx.rectangle(rect_container.x_origin, rect_container.y_origin, size_x, size_y)
        ctx.fill()

        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.rectangle(rect_container.x_origin, rect_container.y_origin, size_x, size_y)
        ctx.stroke()

        ctx.set_operator(cairo.OPERATOR_OVER)

        ctx.set_source_rgba(*rect_container.edge_color)
        ctx.rectangle(rect_container.x_origin, rect_container.y_origin, size_x, size_y)
        ctx.stroke()

    def draw(self, ctx):
        for rect in self.strokes:
            self.draw_rect(ctx, rect)

    def finish(self, veil):
        self.active_stroke = None

    def undo(self):
        if len(self.strokes) > 0:
            self.strokes.pop()
