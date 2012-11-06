gnome-shell-search-github-repositories
======================================

Search through your own github repositories by name in the gnome shell.

Installing
----------

Only available for gnome-shell-3.6 and later (Fedora 18 and later)::

    yum -y install gnome-shell-search-github-repositories

Configuration
-------------

The search provider *will not work* without being configured.

Create a file in your homedirectory at ``~/.search-github`` with the
following content::

  [github]
  username = YOUR_USERNAME
  password = YOUR_PASSWORD

