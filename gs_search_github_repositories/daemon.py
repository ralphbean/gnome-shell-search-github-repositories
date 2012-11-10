# This file is a part of search-githubrepos.
#
# search-githubrepos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# search-githubrepos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with search-githubrepos.  If not, see
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
import os
import urllib
import webbrowser

from gi.repository import Gio
import gobject

import githubutils


config_tool = "gnome-shell-search-github-repositories-config"

# Convenience shorthand for declaring dbus interface methods.
# s.b.n. -> search_bus_name
search_bus_name = 'org.gnome.Shell.SearchProvider'
sbn = dict(dbus_interface=search_bus_name)


class SearchGithubRepositoriesService(dbus.service.Object):
    """ The GithubRepositories Search Daemon.

    This service is started through DBus activation by calling the
    :meth:`Enable` method, and stopped with :meth:`Disable`.

    """
    bus_name = 'org.gnome.githubrepositories.search'
    enabled = False

    icon_tmpl = "https://secure.gravatar.com/avatar/%s"
    http_prefix = "https://github.com"

    # 1 file System cache
    _icon_cache_dir = os.path.expanduser("~/.cache/search-github-repos/")

    # 3 in-memory caches
    _icon_cache = {}
    _search_cache = {}
    _request_cache = {}

    _object_path = '/%s' % bus_name.replace('.', '/')
    __name__ = "SearchGithubRepositoriesService"

    def __init__(self):
        self.settings = Gio.Settings.new(self.bus_name)
        if not self.settings.get_boolean('enabled'):
            return

        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)
        self._initialize_icon_cache()
        self.enabled = True

    @dbus.service.method(in_signature='s', **sbn)
    def ActivateResult(self, search_id):
        webbrowser.open(self.http_prefix + "/" + search_id.split(':')[0])

    @dbus.service.method(in_signature='as', out_signature='as', **sbn)
    def GetInitialResultSet(self, terms):
        return self._basic_search(terms)

    @dbus.service.method(in_signature='as', out_signature='aa{sv}', **sbn)
    def GetResultMetas(self, ids):
        return [dict(
            id=id,
            name=id.split(":")[0].split('/')[-1],
            gicon=self.iconify(id.split(":")[-1]),
        ) for id in ids]

    @dbus.service.method(in_signature='asas', out_signature='as', **sbn)
    def GetSubsearchResultSet(self, previous_results, new_terms):
        return self._basic_search(new_terms)

    def iconify(self, filetoken):
        filename = self._icon_cache.get(filetoken)

        # If its not in our in-memory cache, then we assume it is also not on
        # disk in the _icon_cache_dir.  Grab it, save it to the fs, and cache
        # the association.
        if not filename:
            url = self.icon_tmpl % filetoken
            filename = self._icon_cache_dir + filetoken
            urllib.urlretrieve(url, filename)
            self._icon_cache[filetoken] = filename

        return filename

    def _initialize_icon_cache(self):
        if not os.path.isdir(self._icon_cache_dir):
            os.mkdir(self._icon_cache_dir)

        # Populate our in-memory cache from the file system
        for filename in os.listdir(self._icon_cache_dir):
            self._icon_cache[filename] = self._icon_cache_dir + filename

    def _basic_search(self, terms):
        term = ''.join(terms)

        def __build_rows(username, auth):
            if username not in self._request_cache:
                repos = githubutils.get_all(username, auth, "repos")
                self._request_cache[username] = repos

            repos = self._request_cache[username]
            matches = [r for r in repos if term in r['full_name']]
            rows = [r['full_name'] + ":" + r['owner']['gravatar_id']
                    for r in matches]
            return rows

        if not term in self._search_cache:
            username, password = auth = githubutils.load_auth()

            # Not configured.. ~/.search-github is busted.
            if not username:
                # FIXME - this isn't totally working.
                os.system(config_tool)
                return []

            rows = __build_rows(username, auth)
            for org in githubutils.get_all(username, auth, "orgs"):
                rows += __build_rows(org['login'], auth)

            self._search_cache[term] = rows

        return self._search_cache[term]


def main():
    service = SearchGithubRepositoriesService()
    loop = gobject.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
