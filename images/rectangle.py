import cairo
from images.image import Image


class RectangleImage(Image):
    def __init__(self, edge_width, edge_color, fill_color, x, y):
        super(RectangleImage, self).__init__()
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.x_origin = x
        self.y_origin = y

        self.x_current = x
        self.y_current = y

        if self.edge_color is None:
            self.edge_color = self.random_color(0.7)
        if self.fill_color is None:
            self.fill_color = self.random_color(0.2)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        size_x = self.x_current - self.x_origin
        size_y = self.y_current - self.y_origin
        ctx.set_line_width(self.edge_width)

        ctx.set_source_rgba(*self.fill_color)
        ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
        ctx.fill()

        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
        ctx.stroke()

        ctx.set_operator(cairo.OPERATOR_OVER)

        ctx.set_source_rgba(*self.edge_color)
        ctx.rectangle(self.x_origin, self.y_origin, size_x, size_y)
        ctx.stroke()