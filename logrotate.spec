# TODO
# - bug: when logrotate.status is written truncated (due disk getting full) and
#   the line is partial, it will complain erronously that the line is too long
#   while it just doesn't have the second DATE column. and that error should be
#   ignored as warning not fatal as error.
#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
#
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
Version:	3.7.7
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://fedorahosted.org/releases/l/o/logrotate/%{name}-%{version}.tar.gz
# Source0-md5:	431e135abb7f3fe19de4c6a65bb66823
Source1:	%{name}.conf
Source2:	%{name}.sysconfig
Patch0:		%{name}-man.patch
Patch1:		%{name}-cron.patch
URL:		https://fedorahosted.org/logrotate/
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
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	WITH_SELINUX=%{?with_selinux:yes}%{!?with_selinux:no} \
	STATEFILE="%{statdir}/logrotate.status"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_mandir},%{statdir},/var/log/archive}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/logrotate
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate
> $RPM_BUILD_ROOT%{statdir}/logrotate.status
> $RPM_BUILD_ROOT/var/log/archiv

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %ghost %{statdir}/logrotate.status
%attr(750,root,logs) %dir /var/log/archive
%ghost /var/log/archiv
%{_mandir}/man8/*
