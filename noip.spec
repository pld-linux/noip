# TODO: init script, config file sample
Summary:	noip - Linux client for the no-ip.com dynamic DNS service
Summary(pl):	noip - linuksowy klient serwisu dynamicznego DNS no-ip.com
Name:		noip
Version:	2.0.12
Release:	0.1
Epoch:		0
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.no-ip.com/client/linux/%{name}-%{version}.tar.gz
# Source0-md5:	72053672a5125d39b861a130aa4532f1
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-config_location.patch
URL:		http://www.no-ip.com/
Requires:	rc-scripts
Requires(pre,post):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
noip - Linux client for the no-ip.com dynamic DNS service.

%description -l pl
noip - linuksowy klient serwisu dynamicznego DNS no-ip.com .

%prep
%setup -q
%patch0 -p1
%patch1 -p1
mv -f %{name}2.c %{name}.c

%build

%{__make} \
	PREFIX=%{_prefix} CONFDIR=%{_sysconfdir} \
	CC="%{__cc}" \
	    CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	CONFDIR=%{_sysconfdir} \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
touch $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
    /etc/rc.d/init.d/%{name} restart 1>&2
else
    echo "Run \"/etc/rc.d/init.d/%{name} start\" to start noip daemon."
fi

%preun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} stop 1>&2
    fi
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README.FIRST
%attr(755,root,root) %{_bindir}/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
