Summary:	Rotates, compresses, and mails system logs.
Summary(de):	Rotiert, komprimiert und verschickt Systemlogs.
Summary(fr):	Fait tourner, compresse, et envoie par mail les connexions au système.
Summary(pl):	Rotacje, kompresowanie, i system logowania.
Summary(tr):	Sistem günlüklerini yönlendirir, sýkýþtýrýr ve mektup olarak yollar.
Name:		logrotate
Version:	3.2
Release:	4
Copyright:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
URL:		ftp://ftp.redhat.com/pub/redhat/code/logrotate
Source:		%{name}-%{version}.tar.gz
Patch0:		logrotate-pld.patch
Patch1:		logrotate-fhs.patch
BuildRequires:	popt-devel >= 1.3
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
%setup  -q
%patch0 -p1
%patch1 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d}

make PREFIX=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT/usr/man/man8 $RPM_BUILD_ROOT%{_mandir}

install examples/logrotate.conf.pld $RPM_BUILD_ROOT/etc/logrotate.conf
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.gz

%attr(755,root,root) %{_sbindir}/logrotate
%attr(750,root,root) /etc/cron.daily/logrotate
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/*.conf
%attr(750,root,root) %dir /etc/logrotate.d

%{_mandir}/man8/*
