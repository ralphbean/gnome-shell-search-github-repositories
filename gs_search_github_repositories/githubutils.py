""" Tools for querying github.

I tried using pygithub3, but it really sucks.
"""

import os
import ConfigParser
import requests


def _link_field_to_dict(field):
    """ Utility for ripping apart github's Link header field.
    It's kind of ugly.
    """

    if not field:
        return dict()

    return dict([
        (
            part.split('; ')[1][5:-1],
            part.split('; ')[0][1:-1],
        ) for part in field.split(', ')
    ])


def load_auth():
    """ We expect the user to keep a config file for us.

    This is kind of a bummer.  It would be awesome if we could keep this in
    gnome-shell's Online Accounts thing, but I guess they built that as a Silo
    on purpose (for some reason).  It's not pluggable so we can't just DIY
    without diving into gnome-shell proper.  Gotta do that some day, I guess.
    """

    # TODO -- consider using ~/.local/hub and share with the hub package
    filename = os.path.expanduser("~/.search-github")
    parser = ConfigParser.ConfigParser()
    parser.read(filename)
    try:
        username = parser.get('github', 'username')
        password = parser.get('github', 'password')
        return username, password
    except:
        return None, None


def get_all(username, auth, item="repos"):
    """ username should be a string
    auth should be a tuple of username and password.

    item can be one of "repos" or "orgs"
    """

    valid_items = ["repos", "orgs"]
    if item not in valid_items:
        raise ValueError("%r is not one of %r" % (item, valid_items))

    tmpl = "https://api.github.com/users/{username}/{item}?per_page=100"
    url = tmpl.format(username=username, item=item)
    results = []
    link = dict(next=url)
    while 'next' in link:
        response = requests.get(link['next'], auth=auth)
        if response.status_code != 200:
            raise IOError("Non-200 status code %r" % response.status_code)

        results += response.json
        link = _link_field_to_dict(response.headers['link'])

    return results
