%define		svnrev	520
%define		rel		1
%define		plugin	check_libs
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin to check inexistent libraries in running processes
Name:		nagios-plugin-%{plugin}
Version:	0.1
Release:	0.%{svnrev}.%{rel}
License:	BSD
Group:		Networking
Source0:	http://svn.noreply.org/svn/weaselutils/trunk/nagios-check-libs
# Source0-md5:	fea660b5fb4cf5759b7fc47084c94d48
Source1:	http://svn.noreply.org/svn/weaselutils/trunk/nagios-check-libs.conf
# Source1-md5:	dae6d27674df15d9647c58606e3c5da8
Source2:	%{plugin}.cfg
URL:		http://svn.noreply.org/svn/weaselutils/trunk/
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	sed >= 4.0
# for reading .conf
Requires:	lsof
Suggests:	perl-YAML-Syck
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

%{__sed} -i -e 's,/etc/nagios/check-libs.conf,%{_sysconfdir}/%{plugin}.conf,' %{plugin}.pl

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
