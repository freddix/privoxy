Summary:	Non-caching web proxy with advanced filtering capabilities
Name:		privoxy
Version:	3.0.21
Release:	2
License:	GPL v2+
Source0:	http://downloads.sourceforge.net/ijbswa/%{name}-%{version}-stable-src.tar.gz
# Source0-md5:	79558f2545cfcf9731f7de611646d837
Source1:	%{name}.logrotate
Source2:	%{name}.service
Patch0:		%{name}-DESTDIR.patch
Group:		Networking/Daemons
URL:		http://www.privoxy.org/
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	pcre-devel
BuildRequires:	perl-base
BuildRequires:	zlib-devel
Requires(pre,postun):	pwdutils
Requires(post,preun,postun):	systemd-units
Provides:	group(privoxy)
Provides:	user(privoxy)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Privoxy is a web proxy with advanced filtering capabilities for
protecting privacy, filtering web page content, managing cookies,
controlling access, and removing ads, banners, pop-ups and other
obnoxious Internet junk. Privoxy has a very flexible configuration and
can be customized to suit individual needs and tastes. Privoxy has
application for both stand-alone systems and multi-user networks.

%prep
%setup -qn %{name}-%{version}-stable
%patch0 -p1

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure \
	--enable-compression
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CONF_BASE=%{_sysconfdir}/privoxy \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/privoxy
install -D %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/privoxy.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 111 privoxy
%useradd -u 111 -d %{_sysconfdir}/privoxy -s /usr/bin/false -c "Privoxy user" -g privoxy privoxy

%post
%systemd_post privoxy.service

%preun
%systemd_preun privoxy.service

%postun
if [ "$1" = "0" ]; then
	%userremove privoxy
	%groupremove privoxy
fi
%systemd_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/privoxy

%dir %attr(751,root,privoxy) %{_sysconfdir}/privoxy
%dir %attr(751,root,privoxy) %{_sysconfdir}/privoxy/templates
%attr(640,root,privoxy) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/privoxy/*.*
%attr(640,root,privoxy) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/privoxy/config
%attr(640,root,privoxy) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/privoxy/templates/*
%attr(640,root,privoxy) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/privoxy/trust
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/privoxy

%dir %attr(751,privoxy,privoxy) /var/log/privoxy
%attr(640,privoxy,privoxy) %ghost %verify(not md5 mtime size) /var/log/privoxy/*

%{systemdunitdir}/privoxy.service

%{_docdir}/privoxy
%{_mandir}/man1/privoxy.1*

