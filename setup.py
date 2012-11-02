from setuptools import setup

requires = [
    'pkgwat.api',
]

setup(
    name="gnome-shell-search-fedora-packages",
    version='1.0.0rc1',
    description="A gnome shell search provider for apps.fp.o/packages",
    url="http://github.com/ralphbean/gnome-shell-search-fedora-packages",
    author="Ralph Bean",
    author_email="rbean@redhat.com",
    license='GPLv3',
    install_requires=requires,
    packages=['gs_search_fedora_packages'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gnome-shell-search-fedora-packages-daemon = gs_search_fedora_packages.daemon:main',
        ],
    }
)
