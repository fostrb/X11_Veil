import cairo
from tools.brushes import Brush
from math import pi, hypot


class PolygonImage():
    def __init__(self, origin, edge_width, edge_color, fill_color, sensitivity):
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

    def determine_distance_eligible(self):
        if hypot(self.x_current - self.x_origin, self.y_current - self.y_origin) < self.sensitivity:
            self.is_in_complete_range = True
        else:
            self.is_in_complete_range = False

    def determine_complete_eligibile(self):
        if len(self.points) >= 3:
            self.is_complete_eligible = True
        else:
            self.is_complete_eligible = False


class NewPolygonBrush(Brush):
    def __init__(self, edge_width=3, edge_color=None, fill_color=None, sensitivity=20):
        super(NewPolygonBrush, self).__init__()
        self.sensitivity = sensitivity
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.active_stroke = None
        self.images = []

    def mouse_primary(self, veil, event):
        if not self.active_stroke:
            self.active_stroke = PolygonImage(event, self.edge_width, self.edge_color, self.fill_color, self.sensitivity)
            if not self.edge_color:
                self.active_stroke.edge_color = self.random_color_transparent(.7)
            if not self.fill_color:
                self.active_stroke.fill_color = self.random_color_transparent(.2)
            self.images.append(self.active_stroke)
            self.capturing_movement = True
        else:
            pass

    def mouse_move(self, veil, event):
        if self.active_stroke:
            self.active_stroke.x_current = event.x
            self.active_stroke.y_current = event.y
            self.active_stroke.determine_distance_eligible()
            self.active_stroke.determine_complete_eligibile()
            veil.queue_draw()

    def mouse_release(self, veil, event):
        if not self.active_stroke:
            return
        if len(self.active_stroke.points) == 0:
            self.active_stroke.x_origin = event.x
            self.active_stroke.y_origin = event.y
            self.active_stroke.points.append((event.x, event.y))

        elif self.active_stroke.is_in_complete_range:
            if self.active_stroke.is_complete_eligible:
                self.active_stroke.x_current = self.active_stroke.x_origin
                self.active_stroke.y_current = self.active_stroke.y_origin
                self.active_stroke.is_complete = True
                self.active_stroke = None
        else:
            self.active_stroke.points.append((self.active_stroke.x_current, self.active_stroke.y_current))
            self.active_stroke.determine_complete_eligibile()

        veil.queue_draw()

    def mouse_secondary(self, veil, event):
        #self.cancel(veil)
        pass



    def draw_polygon(self, image, ctx):
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(self.edge_width)

        if len(image.points) < 1:
            ctx.set_source_rgba(1, 0, 0, .5)
            ctx.arc(image.x_current, image.y_current, image.sensitivity, 0, 2 * pi)
            ctx.fill()
            ctx.set_source_rgba(0, 1, 0, .5)
            ctx.arc(image.x_current, image.y_current, image.sensitivity, 0, 2 * pi)
            ctx.stroke()

        elif not image.is_complete:
            if image.is_in_complete_range:
                if image.is_complete_eligible:
                    ctx.set_source_rgba(0, 1, 0, .5)
                else:
                    ctx.set_source_rgba(1, 0, 0, .5)
            else:
                ctx.set_source_rgba(1, 1, 1, .5)

            ctx.arc(image.x_origin, image.y_origin, image.sensitivity, 0, 2 * pi)
            ctx.fill()
            ctx.set_source_rgba(0, 1, 0, .5)
            ctx.arc(image.x_origin, image.y_origin, image.sensitivity, 0, 2 * pi)
            ctx.stroke()

        else:
            ctx.set_source_rgba(*image.fill_color)
            ctx.move_to(image.x_origin, image.y_origin)

            for point in image.points:
                ctx.line_to(*point)
            if len(image.points) > 1:
                ctx.line_to(image.x_current, image.y_current)
            ctx.fill()

        ctx.set_source_rgba(*image.edge_color)

        ctx.move_to(image.x_origin, image.y_origin)

        for point in image.points:
            ctx.line_to(*point)

        if len(image.points) >= 1:
            ctx.line_to(image.x_current, image.y_current)
        ctx.stroke()

    def draw(self, ctx):
        for image in self.images:
            self.draw_polygon(image, ctx)

    def undo(self):
        if len(self.images) > 0:
            self.images.pop()
