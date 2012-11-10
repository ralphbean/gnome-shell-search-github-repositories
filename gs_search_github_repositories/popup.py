""" Pop up a dialog to get the user's username and password. """

from gi.repository import Gtk

import os
import sys
import keyring


class Handler(object):
    window = None
    username = None
    password = None

    def save_username(self, entry):
        self.username = entry.get_text()

    def save_password(self, entry):
        self.password = entry.get_text()

    def on_activate(self, button):
        if self.username and self.password:
            self.save_creds(self.username, self.password)

        self.destroy()

    def on_close(self, *args, **kw):
        self.destroy()

    def destroy(self):
        self.window.destroy()
        Gtk.main_quit()

    def save_creds(self, username, password):
        keyring.set_password("github-search", "username", username)
        keyring.set_password("github-search", "password", password)


class lock_file(object):
    dname = os.path.expanduser("~/.cache/search-github-repos/")
    fname = dname + "popup.pid"

    def __enter__(self, *args, **kw):
        if not os.path.exists(self.dname):
            os.mkdir(self.dname)

        if os.path.exists(self.fname):
            raise IOError("Another instance appears to be running.")

        with open(self.fname, "w") as f:
            f.write(str(os.getpid()))

    def __exit__(self, *args, **kw):
        os.remove(self.fname)


def main():
    with lock_file():
        builder = Gtk.Builder()
        fname = "/usr/share/gnome-shell-search-github/popup.glade"

        if os.path.exists("data/popup.glade"):
            builder.add_from_file("data/popup.glade")
        else:
            builder.add_from_file(fname)

        builder.connect_signals(Handler())

        window = builder.get_object("window1")
        window.show_all()
        Handler.window = window

        Gtk.main()


if __name__ == '__main__':
    sys.exit(main())
