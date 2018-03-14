import cairo
from tools.brushes import Brush
from math import pi, hypot


class PolygonBrush(Brush):
    def __init__(self, event, edge_width=3, edge_color=None, fill_color=None, sensitivity=20):
        super(PolygonBrush, self).__init__()
        self.sensitivity = sensitivity
        self.edge_width = edge_width

        self._complete_eligible = False
        self._in_complete_range = True
        self._is_complete = False
        if edge_color:
            self.edge_color = edge_color
        else:
            self.edge_color = self.random_color_transparent(.7)
        if fill_color:
            self.fill_color = fill_color
        else:
            self.fill_color = self.random_color_transparent(.2)

        self.x_origin = event.x
        self.y_origin = event.y

        self.x_current = event.x
        self.y_current = event.y

        self.points = []
        self.capturing_movement = True

    def mouse_move(self, veil, event):
        self.x_current = event.x
        self.y_current = event.y

        distance_from_origin = hypot(self.x_current - self.x_origin, self.y_current - self.y_origin)

        if distance_from_origin < self.sensitivity:
            self._in_complete_range = True
        else:
            self._in_complete_range = False
        veil.queue_draw()

    '''
    def mouse_primary(self, veil, event):
        if self._in_complete_range & self._complete_eligible:
            self.x_current = self.x_origin
            self.y_current = self.y_origin
            self._is_complete = True
            self.finish(veil)
        else:
            self.polygon.append((self.x_current, self.y_current))
        if len(self.polygon) > 2:
            self._complete_eligible = True
        veil.queue_draw()
    '''

    def mouse_release(self, veil, event):
        if len(self.points) == 0:
            self.x_origin = event.x
            self.y_origin = event.y
            self.add_point(self.x_origin, self.y_origin)

        elif self._in_complete_range:
            if self._complete_eligible:
                self.x_current = self.x_origin
                self.y_current = self.y_origin
                self._is_complete = True
                self.POINTS_DRAGGABLE = True
                self.finish(veil)

                if not self._complete_eligible:
                    pass

        else:
            self.add_point(self.x_current, self.y_current)
            if len(self.points) > 2:
                self._complete_eligible = True

        veil.queue_draw()

    def mouse_secondary(self, veil, event):
        self.cancel(veil)

    def draw(self, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(self.edge_width)

        if len(self.points) < 1:
            ctx.set_source_rgba(1, 0, 0, .5)
            ctx.arc(self.x_current, self.y_current, self.sensitivity, 0, 2 * pi)
            ctx.fill()
            ctx.set_source_rgba(0, 1, 0, .5)
            ctx.arc(self.x_current, self.y_current, self.sensitivity, 0, 2 * pi)
            ctx.stroke()

        elif not self._is_complete:
            if self._in_complete_range:
                if self._complete_eligible:
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

        ctx.set_source_rgba(*self.edge_color)

        ctx.move_to(self.x_origin, self.y_origin)

        for point in self.points:
            ctx.line_to(*point)

        if len(self.points) >= 1:
            ctx.line_to(self.x_current, self.y_current)
        ctx.stroke()

    def add_point(self, x, y):
        if (x, y) not in self.points:
            self.points.append((x, y))
