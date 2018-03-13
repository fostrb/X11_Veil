from utils.brushes import *
import gi; gi.require_version('Gtk', '3.0')
import cairo
from gi.repository import Gtk, Gdk


class BrushSelector(Gtk.Window):
    def __init__(self, veil):
        super(BrushSelector, self).__init__()
        #self.connect('button-press-event', self.mouse_press)
        #self.set_events(self.get_events() | Gdk.EventMask.BUTTON_PRESS_MASK)
        #self.set_decorated(False)
        self.set_keep_above(True)

        veilsize = veil.get_size()
        self.show()
