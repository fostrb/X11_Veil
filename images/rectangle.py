import cairo
from images.image import Image


class RectangleImage(Image):
    def __init__(self, edge_width, edge_color, fill_color, x, y, glow=0):
        super(RectangleImage, self).__init__()
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.x_origin = x
        self.y_origin = y

        self.x_current = x
        self.y_current = y

        self.glow = glow
        self.gradient = None

        if self.edge_color is None:
            self.edge_color = self.random_color(0.7)
        if self.fill_color is None:
            self.fill_color = self.random_color(0.2)

    def set_glow(self, glow):
        self.glow = glow
        self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)
            ctx.set_operator(cairo.OPERATOR_ADD)
        else:
            ctx.set_operator(cairo.OPERATOR_OVER)

        size_x = self.x_current - self.x_origin
        size_y = self.y_current - self.y_origin

        ctx.set_source_rgba(*self.fill_color)
        ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
        ctx.fill()

        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)
            for width, color in self.gradient:
                ctx.set_line_width(width)
                ctx.set_source_rgba(*color)
                ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
                ctx.stroke()
            ctx.set_line_width(self.edge_width / 2)
            ctx.set_source_rgba(1, 1, 1, .5)
            ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
            ctx.stroke()

        else:
            ctx.set_line_width(self.edge_width)
            ctx.set_source_rgba(*self.edge_color)
            ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
            ctx.stroke()