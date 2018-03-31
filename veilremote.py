from dbusinterface import DBUS_NAME
from dbusinterface import DBUS_PATH
from dbusinterface import DbusManager
import argparse
import dbus
import os
import signal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", '--togglevisibility', dest='toggle', action='store_true', default=False, help='Toggles visibility')
    parser.add_argument("-x", '--togglepass', dest='togglepass', action='store_true', default=False, help='Toggles passthrough')
    args = parser.parse_args()

    instance = None
    remote_object = None
    try:
        bus = dbus.SessionBus()
        remote_object = bus.get_object(DBUS_NAME, DBUS_PATH)
        already_running = True
    except dbus.DBusException:
        from veil import Veil
        instance = Veil()
        remote_object = DbusManager(instance)
        already_running = False

    try:
        if args.toggle:
            remote_object.show_hide()

        if args.togglepass:
            remote_object.toggle_passthrough()

        if not already_running:
            remote_object.show_hide()
    except:
        return None
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