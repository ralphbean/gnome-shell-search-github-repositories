from setuptools import setup

requires = [
    'requests',
]

setup(
    name="gnome-shell-search-github-repositories",
    version='1.0.0',
    description="A gnome shell search provider for your github repos",
    url="http://github.com/ralphbean/gnome-shell-search-github-repositories",
    author="Ralph Bean",
    author_email="rbean@redhat.com",
    license='GPLv3',
    install_requires=requires,
    packages=['gs_search_github_repositories'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gnome-shell-search-github-repositories-daemon = gs_search_github_repositories.daemon:main',
            'gnome-shell-search-github-repositories-config = gs_search_github_repositories.popup:main',
        ],
    }
)
