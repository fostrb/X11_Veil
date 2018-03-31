from tools.brushes import Brush
import cairo
from images.line import LineImage


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
        self.images = []
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = LineImage(self.color, self.width, event.x, event.y, event.x, event.y)
            veil.images.append(self.active_stroke)
            #self.images.append(self.active_stroke)
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
        for image in self.images:
            image.draw(ctx)

    def undo(self):
        if len(self.images) > 0:
            self.images.pop()

