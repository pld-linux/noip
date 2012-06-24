# TODO: - initscript or sth. else
Summary:	noip - Linux client for the no-ip.com dynamic DNS service
Summary(pl):	noip - Linuksowy klient serwisu dynamicznego DNS no-ip.com
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the No-IP.com Dynamic DNS update client page.

When configured correctly, the client will check your IP address at a
given time interval checking to see if your IP has changed. If your IP
address has changed it will notify No-IP dns servers and update the IP
corresponding to your No-IP/No-IP+ hostname.

NOTE: You must add hostnames on the website first before you can have
the updater update them.

%description -l pl
To jest klient aktualizuj�cy nasz wpis w systemie No-IP.com

Dobrze skonfigurowany klient b�dzie sprawdza� Tw�j adres IP w
okre�lonych odst�pach czasu, aby wykry� zmiany. Je�li adres IP si�
zmieni, klient poinformuje serwery dns No-IP i zaktualizuje numer IP
odnosz�cy si� do Twojej nazwy hosta w systemie No-IP/No-IP+.

Uwaga: musisz doda� nazwy host�w na stronie (http://www.no-ip.com)
zanim b�dziesz m�g� je aktualizowa� za pomoc tego programu.

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.FIRST
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
