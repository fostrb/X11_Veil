from tools.brushes import *
import signal
import sys
import logging
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GdkX11
import cairo


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
-Tell Veil to toggle active from an external process (and hot-key that to a keypress)

-Brush selector

-DONE: Get signals propagating 'through' veil
-SORTA DONE: Abstract and de-couple drawing before this stuff.
    -Mouse input drawing
        -text input
        -DONE: line by coords
        -DONE: rect by coords
        -DONE: freehand

Fixes:
-Better size-setting for the main gtk window

Aesthetics:
-The bar looks like garbage, mostly the text part.
    -Maybe just make the border a pixel bigger.
-run the 'good' curse removing script


BUGS:
-'button-press-event' being sent twice per click.
'''

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Veil(Gtk.Window):
    def __init__(self, title='veil'):
        super(Veil, self).__init__()
        self.brush_options = [PolygonBrush, FilledRectangleBrush, FreehandBrush, LineBrush]
        self.TEMP_BRUSH_ID = 0

        self.connect("destroy", Gtk.main_quit)
        self.brushes = []
        self.set_title(title)
        self.screen = self.get_screen() # type: GdkX11.X11Screen
        s = Gdk.Screen.get_default()

        self.set_size_request(s.get_width(), s.get_height())  # unresizeable
        self.active_brush = None
        self.transient = False

        visual = self.screen.get_rgba_visual()
        if visual and self.screen.is_composited():
            self.set_visual(visual)
            if self.transient:
                self.input_shape_combine_region(cairo.Region())

        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.connect('draw', self.draw)

        self.fullscreen()

        self.connect('button-press-event', self.mouse_press)
        self.connect('motion-notify-event', self.mouse_move)
        self.connect('button-release-event', self.mouse_release)
        self.connect('key-press-event', self.key_press)
        self.connect('key-release-event', self.key_release)
        self.set_events(self.get_events() |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK |
                        Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.KEY_RELEASE_MASK)
        self.show()

    def toggle_transient(self):
        if self.transient:
            self.input_shape_combine_region(cairo.Region())
            self.transient = True
        else:
            self.input_shape_combine_region(None)
            self.transient = False

    def draw(self, widget, ctx):
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
        self.draw_brushes(ctx)
        if self.transient:
            self.draw_border(ctx)
            #self.draw_header(ctx)

    def draw_brushes(self, ctx):
        for b in self.brushes:
            b.draw(ctx)
        if self.active_brush:
            self.active_brush.draw(ctx)

#-header stuff-----------------------------------------------------------------
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
#------------------------------------------------------------------------------

#-event handling--------------------------------------------------------------
    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            if not self.active_brush:
                self.active_brush = self.brush_options[self.TEMP_BRUSH_ID](event)
            else:
                self.active_brush.mouse_primary(self, event)
        elif event.button == Gdk.BUTTON_SECONDARY:
            if not self.active_brush:
                pass
            else:
                self.active_brush.mouse_secondary(self, event)

    def mouse_move(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            if self.active_brush:
                self.active_brush.mouse_move(self, event)
        elif self.active_brush:
            if self.active_brush.capturing_movement:
                self.active_brush.mouse_move(self, event)

    def mouse_release(self, widget, event):
        if self.active_brush:
            self.active_brush.mouse_release(self, event)

    def key_press(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == 'Escape':
            Gtk.main_quit()
        if Gdk.ModifierType.CONTROL_MASK:
            if key == 'z':
                if len(self.brushes) > 0:
                    self.brushes.pop()
                    self.queue_draw()
            elif key == 'b':
                self.TEMP_BRUSH_ID += 1
                if self.TEMP_BRUSH_ID > len(self.brush_options)-1:
                    self.TEMP_BRUSH_ID = 0

    def key_release(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
#------------------------------------------------------------------------------


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = Veil()
    Gtk.main()
    sys.exit(0)
