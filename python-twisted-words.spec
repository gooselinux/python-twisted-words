%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{python}-twisted-words
Version:        8.2.0
Release:        3.2%{?dist}
Summary:        Twisted Instant Messaging implementations
Group:          Development/Libraries
License:        MIT
URL:            http://twistedmatrix.com/trac/wiki/TwistedWords
Source0:        http://tmrc.mit.edu/mirror/twisted/Words/8.2/TwistedWords-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{python}-twisted-core >= 8.2.0
BuildRequires:  %{python}-devel
Requires:       %{python}-twisted-core >= 8.2.0
Requires:       %{python}-twisted-web

# a noarch-turned-arch package should not have debuginfo
%define debug_package %{nil}

%description
Twisted is an event-based framework for internet applications.

Twisted Words contains implementations of many Instant Messaging protocols,
including IRC, Jabber, MSN, OSCAR (AIM & ICQ), TOC (AOL), and some
functionality for creating bots, inter-protocol gateways, and a client
application for many of the protocols.

In support of Jabber, Twisted Words also contains X-ish, a library for
processing XML with Twisted and Python, with support for a Pythonic DOM and
an XPath-like toolkit.

%prep
%setup -q -n TwistedWords-%{version}

# Fix doc permissions
chmod -x doc/examples/oscardemo.py

%build
%{python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

# This is a pure python package, but extending the twisted namespace from
# python-twisted-core, which is arch-specific, so it needs to go in sitearch
%{python} setup.py install -O1 --skip-build \
    --install-purelib %{python_sitearch} --root $RPM_BUILD_ROOT

# Man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp -a doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
rm -rf doc/man

# See if there's any egg-info
if [ -f $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info ]; then
    echo $RPM_BUILD_ROOT%{python_sitearch}/Twisted*.egg-info |
        sed -e "s|^$RPM_BUILD_ROOT||"
fi > egg-info

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%files -f egg-info
%defattr(-,root,root,-)
%doc README LICENSE doc/* NEWS
%{_bindir}/im
%{_mandir}/man1/im.1*
%{python_sitearch}/twisted/words/
%{python_sitearch}/twisted/plugins/twisted_words.py*

%changelog
* Tue Jan 26 2010 David Malcolm <dmalcolm@redhat.com> - 8.2.0-3.2
- fix source URL

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 8.2.0-3.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.
- Remove no longer installed t-im man page.

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Merge back changes from Paul Howarth.
- Make sure the scriplets never return a non-zero exit status.

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.0-5
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.0-4
- Rebuild for Python 2.6

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.5.0-3
- Handle the egg issue, drop the pyver stuff.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.0-2
- Autorebuild for GCC 4.3

* Fri Aug 31 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.5.0-1
- updated to latest version

* Wed Dec 27 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.0-3
- BR python-devel
- include LICENSE and NEWS

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.0-2
- no longer ghost .pyo files
- rebuild dropin.cache

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.0-1
- new release
- remove xish dependency
- remove noarch

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-2
- disttag

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-0.1.a2
- prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- prep for split

