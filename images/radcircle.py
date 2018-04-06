from images.image import Image
from math import pi
from math import hypot
import cairo


# A circle defined by an origin and a radius;
# while not self.complete: draws a line from center to current mouse location

class RadCircle(Image):
    def __init__(self, origin, edge_width=2, edge_color=None, fill_color=None, glow=0):
        super(RadCircle, self).__init__()
        self.origin = origin
        self.x_origin = int(origin.x)
        self.y_origin = int(origin.y)
        self.x_current = int(origin.x)
        self.y_current = int(origin.y)
        self.complete = False

        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color

        self.glow = glow
        self.gradient = None

        self.radius = 0
        self.set_radius()

        if not self.edge_color:
            self.edge_color = self.random_color(0.7)
        if not self.fill_color:
            self.fill_color = self.random_color(0.2)

    def set_glow(self, glow):
        self.glow = glow
        self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)

    def set_radius(self):
        self.radius = hypot(int(self.x_current) - int(self.x_origin), int(self.y_current) - int(self.y_origin))

    def draw(self, ctx):
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        if not self.complete:
            self.set_radius()
        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)
            ctx.set_operator(cairo.OPERATOR_ADD)
        else:
            ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_source_rgba(*self.fill_color)
        ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi*2)
        ctx.fill()

        if self.glow > 0:
            for width, color in self.gradient:
                ctx.set_line_width(width)
                ctx.set_source_rgba(*color)
                ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi * 2)
                ctx.stroke()
                if not self.complete:
                    ctx.move_to(self.x_origin, self.y_origin)
                    ctx.line_to(self.x_current, self.y_current)
                    ctx.stroke()
            ctx.set_source_rgba(1, 1, 1, .5)
            ctx.set_line_width(self.edge_width / 2)
            ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi * 2)
            ctx.stroke()
            if not self.complete:
                ctx.move_to(self.x_origin, self.y_origin)
                ctx.line_to(self.x_current, self.y_current)
                ctx.stroke()

        else:
            ctx.set_source_rgba(*self.edge_color)
            ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi * 2)
            ctx.stroke()
            if not self.complete:
                ctx.move_to(self.x_origin, self.y_origin)
                ctx.line_to(self.x_current, self.y_current)
                ctx.stroke()
