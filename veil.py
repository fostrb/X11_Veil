import signal
import sys
import logging
import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, xlib, Gdk
from gi.repository import GdkX11
import random
from sys import platform as _platform

if _platform != "linux" or _platform == "linux2":
    sys.exit("No.")

RANDOM_BRUSH_COLORS = True
BRUSH_ALPHA = .5

COLOR_GREEN = (0, 1, 0, BRUSH_ALPHA)
COLOR_RED = (1, 0, 0, BRUSH_ALPHA)

# Veil; Fuck your x11 windows all up
#
# Python3.5
#   gtk, cairo
#
#
# Ben Foster


'''
TODO:
Never thread this. I'm not kidding.
-Add more type hinting for python IDEs

Functionality:
-Tell Veil to toggle active from an external process (and hotkey that to a keypress)

-DONE: Get signals propagating 'through' panes
-SORTA DONE: Abstract and de-couple drawing before this stuff.
    -Mouse input drawing
        -line by coords
        -rect by coords
        -text input
        -DONE: freehand

Fixes:
-Better size-setting for the main gtk window

Aesthetics:
-The bar looks like garbage, mostly the text part.
    -Maybe just make the border a pixel bigger.
-run the 'good' curse removing script
'''


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Brush(object):
    def __init__(self, width, rgba_color):
        self.width = width
        self.rgba_color = rgba_color
        self.stroke = []

    def add_point(self, point):
        self.stroke.append(point)


class Veil(Gtk.Window):
    def __init__(self, title='veil'):
        super(Veil, self).__init__()
        self.CURRENTLY_ACTIVE = True
        self.connect("destroy", Gtk.main_quit)
        self.brushes = []
        self.set_size_request(720, 480) #appears un-resizeable beneath these dimensions; find another function
        self.set_title(title)
        self.screen = self.get_screen() # type: GdkX11.X11Screen

        visual = self.screen.get_rgba_visual()
        if visual and self.screen.is_composited():
            self.set_visual(visual)
            #self.input_shape_combine_region(cairo.Region())

        self.set_decorated(True)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.connect('draw', self.draw_sig)

        #self.fullscreen()

        self.connect('motion-notify-event', self.mouse_move)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event', self.mouse_release)
        self.set_events(self.get_events() |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.show()

    def toggle_active(self):
        if self.CURRENTLY_ACTIVE:
            self.input_shape_combine_region(cairo.Region())
            self.CURRENTLY_ACTIVE = False
        else:
            self.input_shape_combine_region(None)
            self.CURRENTLY_ACTIVE = True

    def draw_sig(self, widget, ctx):
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.fill()
        ##draw shit here
        ctx.set_operator(cairo.OPERATOR_OVER)
        self.brush_draw(ctx)
        if self.CURRENTLY_ACTIVE:
            self.draw_border(ctx)
            self.draw_header(ctx)

    def draw_border(self, ctx):
        ctx.set_line_width(2)
        ctx.set_source_rgb(0, 1, 0)
        ctx.rectangle(0, 0, *self.get_size())
        ctx.stroke()

    def draw_header(self, ctx):
        ctx.set_source_rgb(0, 1, 0)
        ctx.rectangle(0, 0, self.get_size()[0], 16)
        ctx.fill()
        print_text = False
        if print_text:
            ctx.set_source_rgb(0, 0, 0)
            ctx.select_font_face("Inconsolata", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(16)
            ctx.move_to(0, 13)
            ctx.show_text("Veil")
            ctx.stroke()

    def brush_draw(self, cr):
        #cr.set_operator(cairo.OPERATOR_SOURCE)#gets rid over overlap, but problematic with multiple colors
        for brush in self.brushes:
            cr.set_source_rgba(*brush.rgba_color)
            cr.set_line_width(brush.width)
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in brush.stroke:
                cr.line_to(x, y)
            cr.stroke()

    def mouse_move(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            curr_brush = self.brushes[-1]
            curr_brush.add_point((event.x, event.y))
            widget.queue_draw()

    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            if RANDOM_BRUSH_COLORS:
                brush = Brush(10, (random.random(), random.random(), random.random(), 0.5))
            else:
                brush = Brush(10, COLOR_RED)
            brush.add_point((event.x, event.y))
            self.brushes.append(brush)
            widget.queue_draw()
        elif event.button == Gdk.BUTTON_SECONDARY:
            #self.brushes = []
            self.brushes.pop()

    def mouse_release(self, widget, event):
        widget.queue_draw()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = Veil()
    Gtk.main()
    sys.exit(exit_status)
