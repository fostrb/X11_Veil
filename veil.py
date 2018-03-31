from tools.brushes import *
from tools.tool import Tool
import signal
import sys
import logging
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GdkX11
import cairo
#from gi.repository import Vte


# Veil; Fuck your x11 windows all up
#
# Python3.5
#   gtk, cairo
#
#
# Ben Foster


'''
-Add more type hinting for python IDEs

Functionality:
-Better key binding.

-Better brush selector

-Tools:
    -Brushes to write:
        -text input
    -Transformers:
        -Point drag+translate of existing vectors
            --(requires modification of existing Images)
        -Drag individual vectors
            --(requires slight modification of existing Images)
    -Selectors
        -Define scope in relation to other tools and decide if necessary.

Fixes:
-Better size-setting for the main gtk window

Aesthetics:
-The bar looks like garbage, mostly the text part.
    -Maybe just make the border a pixel bigger.


BUGS:
'''

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Veil(Gtk.Window):
    def __init__(self, title='veil'):
        super(Veil, self).__init__()
        self.brush_id = 0
        self.brushes = [PolygonBrush(), FilledRectangleBrush(), LineBrush(), FreehandBrush()]
        self.active_tool = self.brushes[0]
        self.images = []

        self.connect("destroy", Gtk.main_quit)
        self.set_title(title)
        self.screen = self.get_screen() # type: GdkX11.X11Screen
        s = Gdk.Screen.get_default()
        #self.set_size_request(s.get_width(), s.get_height())  # unresizeable
        self.fullscreen()
        self.pass_through = False
        self.hidden = False

        visual = self.screen.get_rgba_visual()
        if visual and self.screen.is_composited():
            self.set_visual(visual)
            if self.pass_through:
                self.input_shape_combine_region(cairo.Region())

        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.connect('draw', self.veil_update)

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

    def toggle_pass_through(self):
        if not self.pass_through:
            self.input_shape_combine_region(cairo.Region())
            self.pass_through = True
        else:
            self.input_shape_combine_region(None)
            self.pass_through = False
        self.queue_draw()

    def show_hide(self):
        if not self.hidden:
            self.hidden = True
            self.unstick()
            self.hide()
        else:
            self.hidden = False
            self.stick()
            self.show_all()

    def veil_update(self, widget, ctx):
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.rectangle(0, 0, *widget.get_size())
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
        self.draw_images(ctx)
        if not self.pass_through:
            self.draw_border(ctx)
            self.draw_header(ctx)

    def execute_tools(self, ctx):
        if self.active_tool:
            if isinstance(self.active_tool, Brush):
                pass

    def draw_images(self, ctx):
        for image in self.images:
            image.draw(ctx)

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
            if not self.active_tool:
                pass
            else:
                self.active_tool.mouse_primary(self, event)
        elif event.button == Gdk.BUTTON_SECONDARY:
            if not self.active_tool:
                pass
            else:
                self.active_tool.mouse_secondary(self, event)

    def mouse_move(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            if self.active_tool:
                self.active_tool.mouse_move(self, event)
        elif self.active_tool:
            if self.active_tool.capturing_movement:
                self.active_tool.mouse_move(self, event)

    def mouse_release(self, widget, event):
        if self.active_tool:
            self.active_tool.mouse_release(self, event)

    def key_press(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == 'Escape':
            Gtk.main_quit()
        if Gdk.ModifierType.CONTROL_MASK:
            if key == 'z':
                self.undo()
                self.queue_draw()
            if key == 'x':
                self.clear()
                self.queue_draw()
            if key == 'b':
                self.brush_id += 1
                if self.brush_id >= len(self.brushes):
                    self.brush_id = 0
                self.active_tool = self.brushes[self.brush_id]
        if key == 'space':
            self.brush_id += 1
            if self.brush_id >= len(self.brushes):
                self.brush_id = 0
            self.active_tool = self.brushes[self.brush_id]
            print(self.active_tool.name)

    def key_release(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
#------------------------------------------------------------------------------


#-veil internal macros---------------------------------------------------------
    def undo(self):
        if len(self.images) > 0:
            self.images.pop()
            if self.active_tool:
                self.active_tool.active_stroke = None

    def clear(self):
        self.images = []
#------------------------------------------------------------------------------


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = Veil()
    #Gtk.main()
    sys.exit(0)
