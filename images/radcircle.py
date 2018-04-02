from images.image import Image
from math import pi
from math import hypot


# A circle defined by an origin and a radius;
# while not self.complete: draws a line from center to current mouse location

class RadCircle(Image):
    def __init__(self, origin, edge_width=2, edge_color=None, fill_color=None):
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

        self.radius = 0
        self.set_radius()

        if not self.edge_color:
            self.edge_color = self.random_color(0.7)
        if not self.fill_color:
            self.fill_color = self.random_color(0.2)

    def set_radius(self):
        self.radius = hypot(int(self.x_current) - int(self.x_origin), int(self.y_current) - int(self.y_origin))

    def draw(self, ctx):
        self.set_radius()
        ctx.set_source_rgba(*self.fill_color)
        ctx.set_line_width(self.edge_width)
        #fill circle
        ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi*2)
        ctx.fill()


        ctx.set_source_rgba(*self.edge_color)
        ctx.arc(self.x_origin, self.y_origin, self.radius, 0, pi * 2)
        #draw outline
        ctx.stroke()

        if not self.complete:
            #draw vector if not finished
            ctx.move_to(self.x_origin, self.y_origin)
            ctx.line_to(self.x_current, self.y_current)
            ctx.stroke()
        #ctx.new_path()