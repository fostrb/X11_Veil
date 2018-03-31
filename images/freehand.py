from images.image import Image
import cairo


class FreehandImage(Image):
    def __init__(self, width, color, points):
        super(FreehandImage, self).__init__()
        self.points = points
        self.width = width
        self.color = color

        if self.color is None:
            self.color = self.random_color(0.5)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgba(*self.color)
        ctx.set_line_width(self.width)
        ctx.new_path()
        for x, y in self.points:
            ctx.line_to(x, y)
        ctx.stroke()
