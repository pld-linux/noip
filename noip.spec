Summary:	noip - Linux client for the no-ip.com dynamic DNS service
Summary(pl.UTF-8):	noip - linuksowy klient serwisu dynamicznego DNS no-ip.com
Name:		noip
Version:	2.1.9
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.no-ip.com/client/linux/%{name}-duc-linux.tar.gz
# Source0-md5:	eed8e9ef9edfb7ddc36e187de867fe64
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-config_location.patch
URL:		http://www.no-ip.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the No-IP.com Dynamic DNS update client page.

When configured correctly, the client will check your IP address at a
given time interval checking to see if your IP has changed. If your IP
address has changed it will notify No-IP DNS servers and update the IP
corresponding to your No-IP/No-IP+ hostname.

NOTE: You must add hostnames on the website (http://www.no-ip.com)
first before you can have the updater update them.

%description -l pl.UTF-8
To jest klient aktualizujący nasz wpis w systemie No-IP.com

Dobrze skonfigurowany klient będzie sprawdzał dany adres IP w
określonych odstępach czasu, aby wykryć zmiany. Jeśli adres IP się
zmieni, klient poinformuje serwery DNS No-IP i zaktualizuje numer IP
odnoszący się do odpowiedniej nazwy hosta w systemie No-IP/No-IP+.

UWAGA: aktualizacja nazw hostów za pomocą tego programu będzie możliwa
po ich dodaniu na stronie (http://www.no-ip.com).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
mv -f %{name}2.c %{name}.c

%build

%{__make} \
	PREFIX=%{_prefix} \
	CONFDIR=%{_sysconfdir} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	CONFDIR=%{_sysconfdir} \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add noip
%service noip restart "noip client daemon"

%preun
if [ "$1" = "0" ]; then
	%service noip stop
	/sbin/chkconfig --del noip
fi

%files
%defattr(644,root,root,755)
%doc README.FIRST
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(4750,root,adm) %{_sbindir}/noip
%attr(754,root,root) /etc/rc.d/init.d/%{name}
