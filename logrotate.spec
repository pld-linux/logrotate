# TODO
# - bug: when logrotate.status is written truncated (due disk getting full) and
#   the line is partial, it will complain erronously that the line is too long
#   while it just doesn't have the second DATE column. and that error should be
#   ignored as warning not fatal as error.
#
# Conditional build:
%bcond_without	acl		# build without ACLs support
%bcond_without	selinux		# build without SELinux support
%bcond_without	tests		# do not perform "make test"

Summary:	Rotates, compresses, removes and mails system log files
Summary(de.UTF-8):	Rotiert, komprimiert und verschickt Systemlogs
Summary(es.UTF-8):	Hace el rutado, comprime y envía mail de logs del sistema
Summary(fr.UTF-8):	Fait tourner, compresse, et envoie par mail les connexions au système
Summary(pl.UTF-8):	System rotacji i kompresowania logów
Summary(pt_BR.UTF-8):	Rotaciona, comprime e envia mail de logs do sistema
Summary(ru.UTF-8):	Ротирует, компрессирует, удаляет и отправляет по почте лог-файлы
Summary(tr.UTF-8):	Sistem günlüklerini yönlendirir, sıkıştırır ve mektup olarak yollar
Summary(uk.UTF-8):	Ротує, компресує, видаляє та відправляє поштою лог-файли
Name:		logrotate
Version:	3.9.1
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	https://fedorahosted.org/releases/l/o/logrotate/%{name}-%{version}.tar.gz
# Source0-md5:	4492b145b6d542e4a2f41e77fa199ab0
Source1:	%{name}.conf
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Source4:	%{name}.crontab
Patch1:		%{name}-man.patch
Patch2:		tabooext.patch
Patch3:		%{name}-largefile.patch
URL:		https://fedorahosted.org/logrotate/
%{?with_acl:BuildRequires:	acl-devel}
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.13
%if %{with selinux}
BuildRequires:	libselinux-devel
%{?with_tests:BuildRequires:	libselinux-utils}
%endif
BuildRequires:	popt-devel >= 1.3
Requires(post):	coreutils
Requires:	coreutils
Requires:	crondaemon
Requires:	filesystem >= 4.0-4
Requires:	gzip
Requires:	setup >= 2.4.6
Suggests:	/bin/mail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		statdir		/var/lib/misc
%define		_libexecdir	%{_prefix}/lib

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files. Logrotate
allows for the automatic rotation compression, removal and mailing of
log files. Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size. Normally,
logrotate runs as a daily cron job.

%description -l de.UTF-8
Logrotate vereinfacht die Verwaltung von Systemen, die sehr viele
Log-Dateien erzeugen, indem es das automatische Rotieren,
Komprimieren, Entfernen, und Senden von Log-Dateien ermöglicht. Jede
Log-Datei kann täglich, wöchentlich oder monatlich verarbeitet werden,
wenn sie zu groß wird.

%description -l es.UTF-8
Logrotate fue proyectado para facilitar la administración de sistemas
que generan gran número de archivos de log. Permite automatización en
la rotación, compresión, remoción y envío de mail de archivos de logs.
Cada archivo de log puede ser tratado diariamente, semanalmente,
mensualmente o cuanto crezca demasiado.

%description -l fr.UTF-8
Logrotate est conçu pour faciliter l'administration de systèmes qui
générent un grand nombre de fichiers de \"log\". Il permet le
roulement, la suppréssion la compression et l'envoi automatiques de
ces fichiers. Chaque fichier de \"log\" peut être pris en charge de
manière quotidienne, hebdomadaire, mensuelle, ou quand il devient trop
volumineux.

%description -l pl.UTF-8
Logrotate jest przeznaczony do łatwej administracji plikami logów.
Program ten pozwala na automatyczną kompresję logów. Może kontrolować
logi raz dziennie, raz na miesiąc, raz na tydzień lub wtedy kiedy
pliki z logami systemowymi są już duże.

%description -l pt_BR.UTF-8
Logrotate foi projetado para facilitar a administração de sistemas que
geram grande número de arquivos de log. Permite automatização na
rotação, compressão, remoção e envio de mail de arquivos de logs. Cada
arquivo de log pode ser tratado diariamente, semanalmente, mensalmente
ou quanto crescer demais.

%description -l ru.UTF-8
Logrotate предназначен для облегчения администрирования системы,
которая генерирует большое количество файлов с логами. Он позволяет
автоматически ротировать, компрессировать, удалять и посылать файлы с
логами по e-mail. Каждый лог может обрабатываться ежедневно,
еженедельно, ежемесячно или по достижении определенного размера.

%description -l tr.UTF-8
logrotate çok fazla sayıda günlük dosyası üreten sistemlerin
yönetimini kolaylaştırmak için tasarlanmıştır. Kayıt dosyalarının
otomatik olarak yönlendirilmesini, sıkıştırılmasını, silinmesinı ve
mektup olarak yollanmasını sağlar. Her dosya günlük, haftalık, aylık
olarak ya da çok büyük boyutlara ulaştığında işlenebilir.

%description -l uk.UTF-8
Logrotate призначений для полегшення адміністрування системи, яка
генерує велику кількість файлів з логами. Він дозволяє автоматично
ротувати, компресувати, видаляти та посилати поштою лог-файли. Кожен
лог може оброблятися щоденно, щотижня, щомісяця або по досягненні
визначеного розміру.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

echo '
#undef STATEFILE
#define STATEFILE "%{statdir}/logrotate.status"
' >> config.h

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--disable-silent-rules \
	--with%{!?with_acl:out}-acl \
	--with%{!?with_selinux:out}-selinux \

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.d,logrotate.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_libexecdir},%{_mandir},%{statdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.d/%{name}
> $RPM_BUILD_ROOT%{statdir}/%{name}.status

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun -- %{name} < 3.8.6-1
# if previous install had /etc/cron.daily/* files unlink (missingok), disable the cronjob
if [ ! -e /etc/cron.daily/%{name} ]; then
	echo DISABLE_LOGROTATE_CRON=yes >> /etc/sysconfig/%{name}
fi

%triggerpostun -- %{name} < 3.7.8-4
%{__sed} -i -e 's,olddir /var/log/archiv$,olddir /var/log/archive,' %{_sysconfdir}/%{name}.conf %{_sysconfdir}/logrotate.d/* || :

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
%attr(755,root,root) %{_libexecdir}/logrotate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(640,root,root) %ghost %{statdir}/logrotate.status
%{_mandir}/man5/logrotate.conf.5*
%{_mandir}/man8/logrotate.8*
