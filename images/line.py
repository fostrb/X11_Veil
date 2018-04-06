from images.image import Image
import cairo


class LineImage(Image):
    def __init__(self, color, width, x_origin, y_origin, x_end, y_end, glow=0):
        super(LineImage, self).__init__()
        self.color = color
        self.width = width
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.x_end = x_end
        self.y_end = y_end

        self.glow = glow
        self.gradient = None

        if self.color is None:
            self.color = self.random_color(0.5)

    def set_glow(self, glow):
        self.glow = glow
        self.gradient = self.make_gradient(self.color, self.width, self.glow)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.color, self.width, self.glow)
            ctx.set_operator(cairo.OPERATOR_ADD)
            for width, color in self.gradient:
                ctx.set_line_width(width)
                ctx.set_source_rgba(*color)

                ctx.move_to(self.x_origin, self.y_origin)
                ctx.line_to(self.x_end, self.y_end)
                ctx.stroke()
            ctx.set_line_width(self.width/2)
            ctx.set_source_rgba(1, 1, 1, .5)
            ctx.move_to(self.x_origin, self.y_origin)
            ctx.line_to(self.x_end, self.y_end)
            ctx.stroke()
        else:
            ctx.set_operator(cairo.OPERATOR_OVER)
            ctx.set_line_width(self.width)
            ctx.set_source_rgba(*self.color)
            ctx.move_to(self.x_origin, self.y_origin)
            ctx.line_to(self.x_end, self.y_end)
            ctx.stroke()
