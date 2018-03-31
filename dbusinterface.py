import dbus
import dbus.glib
import dbus.service

dbus.glib.threads_init()

DBUS_PATH = '/org/veil/RemoteControl'
DBUS_NAME = 'org.veil.RemoteControl'

class DbusManager(dbus.service.Object):
    def __init__(self, veilinstance):
        super(DbusManager, self).__init__()
        self.veil = veilinstance
        self.bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(DBUS_NAME, bus=self.bus)
        super(DbusManager, self).__init__(bus_name, DBUS_PATH)


    @dbus.service.method(DBUS_NAME)
    def show_hide(self):
        self.veil.show_hide()

    @dbus.service.method(DBUS_NAME)
    def toggle_passthrough(self):
        self.veil.toggle_pass_through()