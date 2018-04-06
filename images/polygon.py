from images.image import Image
import cairo
from math import pi, hypot


class PolygonImage(Image):
    def __init__(self, origin, edge_width=5, edge_color=None, fill_color=None, sensitivity=0, glow=0):
        super(PolygonImage, self).__init__()
        self.is_complete_eligible = False
        self.is_in_complete_range = True
        self.is_complete = False
        self.sensitivity = sensitivity
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.x_origin = origin.x
        self.y_origin = origin.y
        self.x_current = origin.x
        self.y_current = origin.y
        self.points = []

        self.glow = glow
        self.gradient = None

        if self.edge_color is None:
            self.edge_color = self.random_color(0.7)
        if self.fill_color is None:
            self.fill_color = self.random_color(0.2)

    def set_glow(self, glow):
        self.glow = glow
        self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)

    def determine_distance_eligible(self):
        if hypot(self.x_current - self.x_origin, self.y_current - self.y_origin) < self.sensitivity:
            self.is_in_complete_range = True
        else:
            self.is_in_complete_range = False

    def determine_complete_eligible(self):
        if len(self.points) >= 4:
            self.is_complete_eligible = True
        else:
            self.is_complete_eligible = False

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        if self.glow > 0:
            if self.gradient is None:
                self.gradient = self.make_gradient(self.edge_color, self.edge_width, self.glow)
            ctx.set_operator(cairo.OPERATOR_ADD)
        else:
            ctx.set_operator(cairo.OPERATOR_OVER)

        ctx.set_line_width(self.edge_width)

        if len(self.points) < 1:
            ctx.set_source_rgba(1, 0, 0, .5)
            ctx.arc(self.x_current, self.y_current, self.sensitivity, 0, 2 * pi)
            ctx.fill()
            ctx.set_source_rgba(0, 1, 0, .5)
            ctx.arc(self.x_current, self.y_current, self.sensitivity, 0, 2 * pi)
            ctx.stroke()

        # 'elif' statement was being evaluated here after previous 'if' evaluated True.
        #       Wrapping it in an 'else' fixed it. I don't get it.
        elif not self.is_complete:
            if self.is_in_complete_range:
                if self.is_complete_eligible:
                    ctx.set_source_rgba(0, 1, 0, .5)
                else:
                    ctx.set_source_rgba(1, 0, 0, .5)
            else:
                ctx.set_source_rgba(1, 1, 1, .5)

            ctx.arc(self.x_origin, self.y_origin, self.sensitivity, 0, 2 * pi)
            ctx.fill()
            ctx.set_source_rgba(0, 1, 0, .5)
            ctx.arc(self.x_origin, self.y_origin, self.sensitivity, 0, 2 * pi)
            ctx.stroke()

        else:
            ctx.set_source_rgba(*self.fill_color)
            ctx.move_to(self.x_origin, self.y_origin)

            for point in self.points:
                ctx.line_to(*point)
            if len(self.points) > 1:
                ctx.line_to(self.x_current, self.y_current)
            ctx.fill()

        if not len(self.points) < 1:
            if self.glow > 0:
                for width, color in self.gradient:
                    ctx.set_line_width(width)
                    ctx.set_source_rgba(*color)
                    ctx.move_to(self.x_origin, self.y_origin)
                    for point in self.points:
                        ctx.line_to(*point)
                    ctx.line_to(self.x_current, self.y_current)
                    ctx.stroke()
                ctx.set_source_rgba(1, 1, 1, .5)
                ctx.set_line_width(self.edge_width/2)
                for point in self.points:
                    ctx.line_to(*point)
                ctx.line_to(self.x_current, self.y_current)
                ctx.stroke()
            else:
                ctx.set_source_rgba(*self.edge_color)

                ctx.move_to(self.x_origin, self.y_origin)

                for point in self.points:
                    ctx.line_to(*point)

                ctx.line_to(self.x_current, self.y_current)
                ctx.stroke()
