from dbusinterface import DBUS_NAME
from dbusinterface import DBUS_PATH
from dbusinterface import DbusManager
import argparse
import dbus
import os
import signal


def main():
    """Parses the command line parameters and decide if dbus methods
    should be called or not. If there is already a guake instance
    running it will be used and a True value will be returned,
    otherwise, false will be returned.
    """
    # Force to xterm-256 colors for compatibility with some old command line programs
    os.environ["TERM"] = "xterm-256color"

    # do not use version keywords here, pbr might be slow to find the version of Guake module
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", '--togglevisibility', dest='toggle', action='store_true', default=False, help='Toggles visibility')
    parser.add_argument("-x", '--togglepass', dest='togglepass', action='store_true', default=False, help='Toggles passthrough')
    args = parser.parse_args()

    instance = None
    # Trying to get an already running instance of Veil. If it is not
    # possible, lets create a new instance. This function will return
    # a boolean value depending on this decision.
    try:
        bus = dbus.SessionBus()
        remote_object = bus.get_object(DBUS_NAME, DBUS_PATH)
        already_running = True
    except dbus.DBusException:
        from veil import Veil
        instance = Veil()
        remote_object = DbusManager(instance)
        already_running = False

    if args.toggle:
        remote_object.show_hide()

    if args.togglepass:
        remote_object.toggle_passthrough()

    if not already_running:
        remote_object.show_hide()
    return already_running


def exec_main():
    if not main():
        #log.debug("Running main gtk loop")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # Load gi pretty late, to speed up as much as possible the parsing of the option for DBus
        # comm through command line
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        Gtk.main()


if __name__ == '__main__':
    exec_main()