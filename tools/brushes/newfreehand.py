import cairo
from tools.brushes.brush import Brush


class FreehandImage():
    def __init__(self, width, color, points):
        self.points = points
        self.width = width
        self.color = color


class NewFreehandBrush(Brush):
    def __init__(self, width=8, color=None):
        super(NewFreehandBrush, self).__init__()
        self.width = width
        self.color = color
        self.images = []
        self.active_stroke = None

    def mouse_primary(self, veil, event):
        if self.active_stroke:
            pass
        else:
            self.active_stroke = FreehandImage(self.width, self.color, [])
            self.active_stroke.points.append((event.x, event.y))
            self.images.append(self.active_stroke)
        if not self.active_stroke.color:
            self.active_stroke.color = self.random_color_transparent(.5)

    def mouse_secondary(self, veil, event):
        pass

    def mouse_move(self, veil, event):
        self.active_stroke.points.append((event.x, event.y))
        veil.queue_draw()

    def mouse_release(self, veil, event):
        self.active_stroke = None
        veil.queue_draw()

    def draw_freehand(self, image, ctx):
        ctx.set_source_rgba(*image.color)
        ctx.set_line_width(image.width)
        ctx.set_line_cap(1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.new_path()
        for x, y in image.points:
            ctx.line_to(x, y)
        ctx.stroke()

    def draw(self, ctx):
        for image in self.images:
            self.draw_freehand(image, ctx)

    def undo(self):
        if len(self.images) > 0:
            self.images.pop()