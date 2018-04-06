from images.image import Image
import cairo


class GlowScribble(Image):
    def __init__(self, width=5, color=None, points=[], glow=0):
        super(GlowScribble, self).__init__()
        self.points = points
        self.width = width
        self.color = color
        self.glow = glow
        self.gradient = None

        if self.color is None:
            self.color = self.random_strong_color(.5)

    def set_glow(self, glow):
        self.glow = glow
        self.gradient = self.make_gradient(self.color, self.width, self.glow)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_operator(cairo.OPERATOR_ADD)
        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.color, self.width, self.glow)
            for width, color in self.gradient:
                ctx.set_line_width(width)
                ctx.set_source_rgba(*color)

                for x, y in self.points:
                    ctx.line_to(x, y)
                ctx.stroke()

            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.set_line_width(self.width/3)
            for x, y in self.points:
                ctx.line_to(x, y)
            ctx.stroke()
        else:
            ctx.set_operator(cairo.OPERATOR_OVER)
            ctx.set_line_width(self.width)
            ctx.set_source_rgba(*self.color)
            for x, y in self.points:
                ctx.line_to(x, y)
            ctx.stroke()
