Summary:	Rotates, compresses, and mails system logs.
Summary(de):	Rotiert, komprimiert und verschickt Systemlogs.
Summary(fr):	Fait tourner, compresse, et envoie par mail les connexions au système.
Summary(pl):	Rotacje, kompresowanie, i system logowania.
Summary(tr):	Sistem günlüklerini yönlendirir, sýkýþtýrýr ve mektup olarak yollar.
Name:		logrotate
Version:	3.2
Release:	2
Copyright:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source:		ftp://ftp.redhat.com/pub/redhat/code/logrotate/%{name}-%{version}.tar.gz
Patch:		logrotate-lastlog.patch
BuildPrereq:	popt-devel >= 1.3
Buildroot:	/tmp/%{name}-%{version}-root

%description
Logrotate is designed to ease administration of systems that generate
large numbers of log files. It allows automatic rotation, compression,
removal, and mailing of log files. Each log file may be handled daily,
weekly, monthly, or when it grows too large.

%description -l de
Logrotate vereinfacht die Verwaltung von Systemen, die sehr viele
Log-Dateien erzeugen, indem es das automatische Rotieren, Komprimieren,
Entfernen, und Senden von Log-Dateien ermöglicht. Jede Log-Datei kann
täglich, wöchentlich oder monatlich verarbeitet werden, wenn sie zu groß wird.

%description -l fr
Logrotate est conçu pour faciliter l'administration de systèmes qui
générent un grand nombre de fichiers de \"log\". Il permet le roulement,
la suppréssion la compression et l'envoi automatiques de ces fichiers.
Chaque fichier de \"log\" peut être pris en charge de manière quotidienne,
hebdomadaire, mensuelle, ou quand il devient trop volumineux. 

%description -l pl
Logrotate jest przeznaczony do ³atwej administracji plikami logów. Program
ten pozwala na automatyczn± kompresjê logów. Mo¿e kontrolowaæ logi raz
dziennie, raz na miesi±c, raz na tydzieñ lub wtedy kiedy pliki z logami
systemowymi s± ju¿ du¿e.

%description -l tr
logrotate çok fazla sayýda günlük dosyasý üreten sistemlerin yönetimini
kolaylaþtýrmak için tasarlanmýþtýr. Kayýt dosyalarýnýn otomatik olarak
yönlendirilmesini, sýkýþtýrýlmasýný, silinmesiný ve mektup olarak
yollanmasýný saðlar. Her dosya günlük, haftalýk, aylýk olarak ya da çok
büyük boyutlara ulaþtýðýnda iþlenebilir.

%prep
%setup -q
%patch -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d}

make PREFIX=$RPM_BUILD_ROOT install
install examples/logrotate-default $RPM_BUILD_ROOT/etc/logrotate.conf
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.gz

%attr(755,root,root) /usr/sbin/logrotate
%attr(750,root,root) /etc/cron.daily/logrotate
%attr(640,root,root) %config /etc/logrotate.conf
%attr(750,root,root) %dir /etc/logrotate.d

%{_mandir}/man8/*

%changelog
* Wed Apr 21 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [3.2-1]
- updated to 3.2,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added full %defattr description in files,
- added %doc,
- removed man group from man pages,
- added passing $RPM_OPT_FLAGS during compile,
- cosmetic changes for common l&f,
- added "BuildPrereq: popt >= 1.3",
- recompiled on rpm 3.

* Tue Oct 06 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.6-4]
- added pl translation,
- minor modifications of the spec file.

* Mon Jun 29 1998 Michael Maher <mike@redhat.com>
- Fixed bug 490, last log shouldn't get rotated.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
