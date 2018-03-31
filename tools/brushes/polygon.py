import cairo
from tools.brushes import Brush
from math import pi, hypot
from images.polygon import PolygonImage

#TODO
# mouse_secondary -> cancel current stroke
#


class PolygonBrush(Brush):
    def __init__(self, edge_width=3, edge_color=None, fill_color=None, sensitivity=20):
        super(PolygonBrush, self).__init__()
        self.name = "Polygon"
        self.sensitivity = sensitivity
        self.edge_width = edge_width
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.active_stroke = None
        self.images = []

    def mouse_primary(self, veil, event):
        if not self.active_stroke:
            self.active_stroke = PolygonImage(event, self.edge_width, self.edge_color, self.fill_color, self.sensitivity)
            #self.images.append(self.active_stroke)
            veil.images.append(self.active_stroke)
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
        if self.active_stroke:
            self.active_stroke = None
            self.images.pop()
            veil.queue_draw()

    def draw(self, ctx):
        for image in self.images:
            image.draw(ctx)

    def undo(self):
        if len(self.images) > 0:
            self.images.pop()
