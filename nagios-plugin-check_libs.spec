%define		plugin	check_libs
Summary:	Nagios plugin to check inexistent libraries in running processes
Name:		nagios-plugin-%{plugin}
Version:	0.2012042101
Release:	1
License:	BSD
Group:		Networking
# https://www.palfrader.org/gitweb/?p=tools/monitoring.git;a=blob_plain;f=nagios-checks/nagios-check-libs;hb=HEAD
Source0:	nagios-check-libs
Source1:	nagios-check-libs.conf
Source2:	%{plugin}.cfg
URL:		https://www.palfrader.org/gitweb/?p=tools/monitoring.git
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	sed >= 4.0
Requires:	lsof
Requires:	perl-YAML-Syck >= 0.97
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to report the usage of no longer existing libraries by
running processes.

%prep
%setup -qcT
cp -p %{SOURCE0} %{plugin}.pl
cp -p %{SOURCE1} %{plugin}.conf

%{__sed} -i -e '
	s,/etc/nagios/check-libs.conf,%{_sysconfdir}/%{plugin}.conf,
	s,libyaml-syck-perl,perl-YAML-Syck,
' %{plugin}.pl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin}.pl $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.conf
%attr(755,root,root) %{plugindir}/%{plugin}
