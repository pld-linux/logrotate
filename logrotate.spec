#
# TODO: test (and eventually fix) dateext and maxage patches

%bcond_without	selinux

#
Summary:	Rotates, compresses, removes and mails system log files
Summary(de):	Rotiert, komprimiert und verschickt Systemlogs
Summary(es):	Hace el rutado, comprime y env�a mail de logs del sistema
Summary(fr):	Fait tourner, compresse, et envoie par mail les connexions au syst�me
Summary(pl):	System rotacji i kompresowania log�w
Summary(pt_BR):	Rotaciona, comprime e envia mail de logs do sistema
Summary(ru):	��������, �������������, ������� � ���������� �� ����� ���-�����
Summary(tr):	Sistem g�nl�klerini y�nlendirir, s�k��t�r�r ve mektup olarak yollar
Summary(uk):	���դ, �������դ, �����Ѥ �� צ������Ѥ ������ ���-�����
Name:		logrotate
Version:	3.7
Release:	2
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	caa28cb5e26db34f7c14236e4058bb5f
Source1:	%{name}.conf
Patch0:		%{name}-man.patch
# patches from ftp://ftp.suse.com/pub/people/ro/logrotate, updated for 3.7
Patch1:		%{name}-dateext.dif
Patch2:		%{name}-maxage.dif
Patch3:		%{name}-noexec-tmp.patch
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	popt-devel >= 1.3
Requires:	/bin/mail
Requires:	crondaemon
Requires(post):	fileutils
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
Komprimieren, Entfernen, und Senden von Log-Dateien erm�glicht. Jede
Log-Datei kann t�glich, w�chentlich oder monatlich verarbeitet werden,
wenn sie zu gro� wird.

%description -l es
Logrotate fue proyectado para facilitar la administraci�n de sistemas
que generan gran n�mero de archivos de log. Permite automatizaci�n en
la rotaci�n, compresi�n, remoci�n y env�o de mail de archivos de logs.
Cada archivo de log puede ser tratado diariamente, semanalmente,
mensualmente o cuanto crezca demasiado.

%description -l fr
Logrotate est con�u pour faciliter l'administration de syst�mes qui
g�n�rent un grand nombre de fichiers de \"log\". Il permet le
roulement, la suppr�ssion la compression et l'envoi automatiques de
ces fichiers. Chaque fichier de \"log\" peut �tre pris en charge de
mani�re quotidienne, hebdomadaire, mensuelle, ou quand il devient trop
volumineux.

%description -l pl
Logrotate jest przeznaczony do �atwej administracji plikami log�w.
Program ten pozwala na automatyczn� kompresj� log�w. Mo�e kontrolowa�
logi raz dziennie, raz na miesi�c, raz na tydzie� lub wtedy kiedy
pliki z logami systemowymi s� ju� du�e.

%description -l pt_BR
Logrotate foi projetado para facilitar a administra��o de sistemas que
geram grande n�mero de arquivos de log. Permite automatiza��o na
rota��o, compress�o, remo��o e envio de mail de arquivos de logs. Cada
arquivo de log pode ser tratado diariamente, semanalmente, mensalmente
ou quanto crescer demais.

%description -l ru
Logrotate ������������ ��� ���������� ����������������� �������,
������� ���������� ������� ���������� ������ � ������. �� ���������
������������� ����������, ���������������, ������� � �������� ����� �
������ �� e-mail. ������ ��� ����� �������������� ���������,
�����������, ���������� ��� �� ���������� ������������� �������.

%description -l tr
logrotate �ok fazla say�da g�nl�k dosyas� �reten sistemlerin
y�netimini kolayla�t�rmak i�in tasarlanm��t�r. Kay�t dosyalar�n�n
otomatik olarak y�nlendirilmesini, s�k��t�r�lmas�n�, silinmesin� ve
mektup olarak yollanmas�n� sa�lar. Her dosya g�nl�k, haftal�k, ayl�k
olarak ya da �ok b�y�k boyutlara ula�t���nda i�lenebilir.

%description -l uk
Logrotate ����������� ��� ���������� ��ͦΦ��������� �������, ���
�����դ ������ ˦��˦��� ���̦� � ������. ��� ������Ѥ �����������
��������, ������������, �������� �� �������� ������ ���-�����. �����
��� ���� ����������� �������, �������, ��ͦ���� ��� �� ��������Φ
����������� ���ͦ��.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	WITH_SELINUX=%{?with_selinux:yes}%{!?with_selinux:no} \
	STATEFILE="%{statdir}/logrotate.status"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d} \
	$RPM_BUILD_ROOT{%{_mandir},%{statdir},/var/log/archiv}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
install examples/logrotate.cron $RPM_BUILD_ROOT/etc/cron.daily/logrotate
> $RPM_BUILD_ROOT%{statdir}/logrotate.status

%clean
rm -rf $RPM_BUILD_ROOT

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
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.conf
%attr(640,root,root) %ghost %{statdir}/logrotate.status
%attr(750,root,root) %dir /var/log/archiv
%{_mandir}/man8/*