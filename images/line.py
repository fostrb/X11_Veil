import cairo
from images.image import Image


class LineImage(Image):
    def __init__(self, color, width, x_origin, y_origin, x_end, y_end):
        super(LineImage, self).__init__()
        self.color = color
        self.width = width
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.x_end = x_end
        self.y_end = y_end

        if self.color is None:
            self.color = self.random_color(0.5)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color)
        ctx.move_to(self.x_origin, self.y_origin)
        ctx.line_to(self.x_end, self.y_end)
        ctx.stroke()
