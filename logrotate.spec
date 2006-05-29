#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
#
Summary:	Rotates, compresses, removes and mails system log files
Summary(de):	Rotiert, komprimiert und verschickt Systemlogs
Summary(es):	Hace el rutado, comprime y envía mail de logs del sistema
Summary(fr):	Fait tourner, compresse, et envoie par mail les connexions au système
Summary(pl):	System rotacji i kompresowania logów
Summary(pt_BR):	Rotaciona, comprime e envia mail de logs do sistema
Summary(ru):	òÏÔÉÒÕÅÔ, ËÏÍÐÒÅÓÓÉÒÕÅÔ, ÕÄÁÌÑÅÔ É ÏÔÐÒÁ×ÌÑÅÔ ÐÏ ÐÏÞÔÅ ÌÏÇ-ÆÁÊÌÙ
Summary(tr):	Sistem günlüklerini yönlendirir, sýkýþtýrýr ve mektup olarak yollar
Summary(uk):	òÏÔÕ¤, ËÏÍÐÒÅÓÕ¤, ×ÉÄÁÌÑ¤ ÔÁ ×¦ÄÐÒÁ×ÌÑ¤ ÐÏÛÔÏÀ ÌÏÇ-ÆÁÊÌÉ
Name:		logrotate
Version:	3.7.4
Release:	0.2
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	73db959389da200b3a0203446e5fe6a6
Source1:	%{name}.conf
Patch0:		%{name}-man.patch
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	popt-devel >= 1.3
Requires(post):	fileutils
Requires:	/bin/mail
Requires:	crondaemon
Requires:	gzip
Requires:	setup >= 2.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		statdir		/var/lib/misc

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

%description -l pt_BR
Logrotate foi projetado para facilitar a administração de sistemas que
geram grande número de arquivos de log. Permite automatização na
rotação, compressão, remoção e envio de mail de arquivos de logs. Cada
arquivo de log pode ser tratado diariamente, semanalmente, mensalmente
ou quanto crescer demais.

%description -l ru
Logrotate ÐÒÅÄÎÁÚÎÁÞÅÎ ÄÌÑ ÏÂÌÅÇÞÅÎÉÑ ÁÄÍÉÎÉÓÔÒÉÒÏ×ÁÎÉÑ ÓÉÓÔÅÍÙ,
ËÏÔÏÒÁÑ ÇÅÎÅÒÉÒÕÅÔ ÂÏÌØÛÏÅ ËÏÌÉÞÅÓÔ×Ï ÆÁÊÌÏ× Ó ÌÏÇÁÍÉ. ïÎ ÐÏÚ×ÏÌÑÅÔ
Á×ÔÏÍÁÔÉÞÅÓËÉ ÒÏÔÉÒÏ×ÁÔØ, ËÏÍÐÒÅÓÓÉÒÏ×ÁÔØ, ÕÄÁÌÑÔØ É ÐÏÓÙÌÁÔØ ÆÁÊÌÙ Ó
ÌÏÇÁÍÉ ÐÏ e-mail. ëÁÖÄÙÊ ÌÏÇ ÍÏÖÅÔ ÏÂÒÁÂÁÔÙ×ÁÔØÓÑ ÅÖÅÄÎÅ×ÎÏ,
ÅÖÅÎÅÄÅÌØÎÏ, ÅÖÅÍÅÓÑÞÎÏ ÉÌÉ ÐÏ ÄÏÓÔÉÖÅÎÉÉ ÏÐÒÅÄÅÌÅÎÎÏÇÏ ÒÁÚÍÅÒÁ.

%description -l tr
logrotate çok fazla sayýda günlük dosyasý üreten sistemlerin
yönetimini kolaylaþtýrmak için tasarlanmýþtýr. Kayýt dosyalarýnýn
otomatik olarak yönlendirilmesini, sýkýþtýrýlmasýný, silinmesiný ve
mektup olarak yollanmasýný saðlar. Her dosya günlük, haftalýk, aylýk
olarak ya da çok büyük boyutlara ulaþtýðýnda iþlenebilir.

%description -l uk
Logrotate ÐÒÉÚÎÁÞÅÎÉÊ ÄÌÑ ÐÏÌÅÇÛÅÎÎÑ ÁÄÍ¦Î¦ÓÔÒÕ×ÁÎÎÑ ÓÉÓÔÅÍÉ, ÑËÁ
ÇÅÎÅÒÕ¤ ×ÅÌÉËÕ Ë¦ÌØË¦ÓÔØ ÆÁÊÌ¦× Ú ÌÏÇÁÍÉ. ÷¦Î ÄÏÚ×ÏÌÑ¤ Á×ÔÏÍÁÔÉÞÎÏ
ÒÏÔÕ×ÁÔÉ, ËÏÍÐÒÅÓÕ×ÁÔÉ, ×ÉÄÁÌÑÔÉ ÔÁ ÐÏÓÉÌÁÔÉ ÐÏÛÔÏÀ ÌÏÇ-ÆÁÊÌÉ. ëÏÖÅÎ
ÌÏÇ ÍÏÖÅ ÏÂÒÏÂÌÑÔÉÓÑ ÝÏÄÅÎÎÏ, ÝÏÔÉÖÎÑ, ÝÏÍ¦ÓÑÃÑ ÁÂÏ ÐÏ ÄÏÓÑÇÎÅÎÎ¦
×ÉÚÎÁÞÅÎÏÇÏ ÒÏÚÍ¦ÒÕ.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	WITH_SELINUX=%{?with_selinux:yes}%{!?with_selinux:no} \
	STATEFILE="%{statdir}/logrotate.status"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d} \
	$RPM_BUILD_ROOT{%{_mandir},%{statdir},/var/log/archive}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate
> $RPM_BUILD_ROOT%{statdir}/logrotate.status
> $RPM_BUILD_ROOT/var/log/archiv

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# change /var/log/archiv to /var/log/archive
if [ ! -L /var/log/archiv ]; then
	if [ -d /var/log/archiv ]; then
		if [ -d /var/log/archive ]; then
			mv /var/log/archiv/* /var/log/archive
			rmdir /var/log/archiv 2>/dev/null || mv -v /var/log/archiv{,.rpmsave}
		else
			mv /var/log/archiv /var/log/archive
		fi
	fi

	# always have archiv symlink (until all packages from Ac use new dir)
	install -d /var/log
	ln -s archive /var/log/archiv
fi
exit 0

%post
if [ -f /var/lib/logrotate.status ]; then
	mv -f /var/lib/logrotate.status %{statdir}/logrotate.status
else
	touch %{statdir}/logrotate.status
	chmod 000 %{statdir}/logrotate.status
	chown root:root %{statdir}/logrotate.status
	chmod 640 %{statdir}/logrotate.status
fi

%files
%defattr(644,root,root,755)
%doc CHANGES
%attr(755,root,root) %{_sbindir}/logrotate
%attr(750,root,root) %dir /etc/logrotate.d
%attr(750,root,root) /etc/cron.daily/logrotate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %ghost %{statdir}/logrotate.status
%attr(750,root,logs) %dir /var/log/archive
%ghost /var/log/archiv
%{_mandir}/man8/*
