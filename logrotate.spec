Summary:	Rotates, compresses, removes and mails system log files
Summary(de):	Rotiert, komprimiert und verschickt Systemlogs
Summary(es):	Hace el rutado, comprime y envía mail de logs del sistema
Summary(fr):	Fait tourner, compresse, et envoie par mail les connexions au système
Summary(pl):	System rotacji i kompresowania logów
Summary(tr):	Sistem günlüklerini yönlendirir, sýkýþtýrýr ve mektup olarak yollar
Name:		logrotate
Version:	3.6
Release:	3
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://ftp.redhat.com/pub/redhat/code/logrotate/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Requires:	/bin/mail
Requires(post):	fileutils
BuildRequires:	popt-devel >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files. Logrotate
allows for the automatic rotation compression, removal and mailing of
log files. Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size. Normally,
logrotate runs as a daily cron job.

%description -l de
Logrotate vereinfacht die Verwaltung von Systemen, die sehr viele
Log-Dateien erzeugen, indem es das automatische Rotieren,
Komprimieren, Entfernen, und Senden von Log-Dateien ermöglicht. Jede
Log-Datei kann täglich, wöchentlich oder monatlich verarbeitet werden,
wenn sie zu groß wird.

%description -l es
Logrotate fue proyectado para facilitar la administración de sistemas
que generan gran número de archivos de log. Permite automatización en
la rotación, compresión, remoción y envío de mail de archivos de logs.
Cada archivo de log puede ser tratado diariamente, semanalmente,
mensualmente o cuanto crezca demasiado.

%description -l fr
Logrotate est conçu pour faciliter l'administration de systèmes qui
générent un grand nombre de fichiers de \"log\". Il permet le
roulement, la suppréssion la compression et l'envoi automatiques de
ces fichiers. Chaque fichier de \"log\" peut être pris en charge de
manière quotidienne, hebdomadaire, mensuelle, ou quand il devient trop
volumineux.

%description -l pl
Logrotate jest przeznaczony do ³atwej administracji plikami logów.
Program ten pozwala na automatyczn± kompresjê logów. Mo¿e kontrolowaæ
logi raz dziennie, raz na miesi±c, raz na tydzieñ lub wtedy kiedy
pliki z logami systemowymi s± ju¿ du¿e.

%description -l tr
logrotate çok fazla sayýda günlük dosyasý üreten sistemlerin
yönetimini kolaylaþtýrmak için tasarlanmýþtýr. Kayýt dosyalarýnýn
otomatik olarak yönlendirilmesini, sýkýþtýrýlmasýný, silinmesiný ve
mektup olarak yollanmasýný saðlar. Her dosya günlük, haftalýk, aylýk
olarak ya da çok büyük boyutlara ulaþtýðýnda iþlenebilir.

%prep
%setup -q

%build
%{__make} CC=%{__cc} RPM_OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{cron.daily,logrotate.d},var/{lib,log/archiv}} \
	$RPM_BUILD_ROOT%{_mandir}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate
> $RPM_BUILD_ROOT/var/lib/logrotate.status

gzip -9nf CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/lib/logrotate.status
chmod 000 /var/lib/logrotate.status
chown root.root /var/lib/logrotate.status
chmod 640 /var/lib/logrotate.status

%files
%defattr(644,root,root,755)
%doc CHANGES.gz
%attr(755,root,root) %{_sbindir}/logrotate
%attr(750,root,root) %dir /etc/logrotate.d
%attr(750,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/cron.daily/logrotate
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.conf
%attr(640,root,root) %ghost /var/lib/logrotate.status
%attr(750,root,root) %dir /var/log/archiv

%{_mandir}/man8/*
