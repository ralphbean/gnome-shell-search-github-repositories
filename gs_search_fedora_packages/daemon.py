# This file is a part of search-fedorapackages.
#
# search-fedorapackages is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# search-fedorapackages is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with search-fedorapackages.  If not, see
# <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2012 Red Hat, Inc.
# Author: Ralph Bean <rbean@redhat.com>


# Acknowledgement - This project was based on a fork from fedmsg-notify
# Copyright (C) 2012 Red Hat, Inc.
# Author: Luke Macken <lmacken@redhat.com>

import dbus
import dbus.glib
import dbus.service

from gi.repository import Gio
import gobject


class SearchFedoraPackagesService(dbus.service.Object):
    """ The FedoraPackages Search Daemon.

    This service is started through DBus activation by calling the
    :meth:`Enable` method, and stopped with :meth:`Disable`.

    """
    bus_name = 'org.fedoraproject.fedorapackages.search'
    msg_received_signal = bus_name + '.MessageReceived'
    enabled = False

    _object_path = '/%s' % bus_name.replace('.', '/')
    __name__ = "SearchFedoraPackagesService"

    def __init__(self):
        self.settings = Gio.Settings.new(self.bus_name)
        if not self.settings.get_boolean('enabled'):
            log.info('Disabled via %r configuration, exiting...' %
                     self.config_key)
            return

        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)
        self.enabled = True

    @dbus.service.method(bus_name)
    def Enable(self, *args, **kw):
        """ A noop method called to activate this service over dbus """

    @dbus.service.method(bus_name)
    def Disable(self, *args, **kw):
        self.__del__()


def main():
    service = SearchFedoraPackagesService()
    gobject.main()

if __name__ == '__main__':
    main()
