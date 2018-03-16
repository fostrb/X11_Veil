import cairo
from tools.brushes import Brush

class LineImage():
    def __init__(self, color, width, x_origin, y_origin, x_end, y_end):
        self.color = color
        self.width = width
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.x_end = x_end
        self.y_end = y_end


class LineBrush(Brush):
    def __init__(self, width=8, color=None):
        super(LineBrush, self).__init__()
        self.name = "Line"
        self.o_color = color
        self.width = width
        if color:
            self.color = color
        else:
            self.color = self.random_color_transparent(.5)
        self.strokes = []
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = LineImage(self.color, self.width, event.x, event.y, event.x, event.y)
            self.strokes.append(self.active_stroke)
            if not self.o_color:
                self.active_stroke.color = self.random_color_transparent(.5)

    def mouse_secondary(self, veil, event):
        #self.cancel(veil)
        pass

    def mouse_move(self, veil, event):
        self.active_stroke.x_end = event.x
        self.active_stroke.y_end = event.y
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.finish(veil)
        veil.queue_draw()

    def finish(self, veil):
        #self.strokes.append(self.active_stroke)
        #self.active_stroke = None
        self.active_stroke = None
        pass

    def draw_line(self, ctx, line_container):
        ctx.set_line_width(line_container.width)
        ctx.set_source_rgba(*line_container.color)
        ctx.move_to(line_container.x_origin, line_container.y_origin)
        ctx.line_to(line_container.x_end, line_container.y_end)
        ctx.stroke()

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for stroke in self.strokes:
            self.draw_line(ctx, stroke)

    def undo(self):
        if len(self.strokes) > 0:
            self.strokes.pop()

