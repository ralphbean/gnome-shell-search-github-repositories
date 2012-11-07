%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %global pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%global modname gs_search_github_repositories
%global busname org.gnome.githubrepositories.search

Name:           gnome-shell-search-github-repositories
Version:        1.0.0
Release:        1%{?dist}
Summary:        Search your Github Repos from the gnome-shell

License:        GPLv3+
URL:            https://github.com/ralphbean/%{name}
Source0:        https://pypi.python.org/packages/source/g/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  pygobject3

Requires:       gnome-shell
Requires:       pygobject3
Requires:       python-requests

%description
gnome-shell-search-github-repositories includes results from your github
repositories in gnome-shell search results.

The search provider *will not work* without being configured.

Create a file in your homedirectory at ~/.search-github with the following
content:

  [github]
  username = YOUR_USERNAME
  password = YOUR_PASSWORD


%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

# Search provider definition
mkdir -p %{buildroot}%{_datadir}/gnome-shell/search-providers
install -m 0644 conf/%{busname}.ini %{buildroot}%{_datadir}/gnome-shell/search-providers/

# DBus configuration
mkdir -p %{buildroot}%{_datadir}/dbus-1/services/
install -m 0644 conf/%{busname}.service \
    %{buildroot}%{_datadir}/dbus-1/services/%{busname}.service
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 conf/%{busname}.conf \
    %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{busname}.conf

# GSettings schema
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
install -m 0644 conf/%{busname}.gschema.xml %{buildroot}%{_datadir}/glib-2.0/schemas

%postun
if [ $1 -eq 0 ]; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc README.rst LICENSE
%{_bindir}/%{name}-daemon

%{python_sitelib}/%{modname}/
%{python_sitelib}/gnome_shell_search_github_repositories-%{version}-py%{pyver}.egg-info/

%{_datadir}/gnome-shell/search-providers/%{busname}.ini
%{_datadir}/dbus-1/services/%{busname}.service
%{_sysconfdir}/dbus-1/system.d/%{busname}.conf
%{_datadir}/glib-2.0/schemas/%{busname}.gschema.xml


%changelog
* Wed Nov 07 2012 Ralph Bean <rbean@redhat.com> - 1.0.0-1
- Search organizations as well.

* Tue Nov 06 2012 Ralph Bean <rbean@redhat.com> - 1.0.0rc2-1
- Proof of concept.
- Read auth from a config file.
- Putting up for fedora review.

* Wed Oct 31 2012 Ralph Bean <rbean@redhat.com> - 1.0.0a-1
- Forked from gnome-shell-search-fedora-packages.

* Tue Oct 30 2012 Luke Macken <lmacken@redhat.com> - 0.3.1-1
- Update our gsettings schema to enable the service once installed.

* Wed Oct 24 2012 Luke Macken <lmacken@redhat.com> - 0.3.0-1
- 0.3.0
- Require fedmsg > 0.5.5 for fedmsg.text.make_processors

* Thu Oct 06 2012 Luke Macken <lmacken@redhat.com> - 0.2.1-1
- 0.2.1 release
- Add the GSettings schema

* Thu Oct 04 2012 Luke Macken <lmacken@redhat.com> - 0.2.0-1
- Initial package.
