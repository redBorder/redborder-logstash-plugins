%global plugins_path /share/logstash-plugins/
%global mac_vendors_path /etc/objects/

Name: redborder-logstash-plugins
Version: %{__version}
Release: %{__release}%{?dist}
BuildArch: noarch
Summary: install redborder logstash plugins

License: AGPL 3.0
URL: https://github.com/redBorder/redborder-logstash-plugins
Source0: %{name}-%{version}.tar

BuildRequires: logstash
Requires: logstash

%description
%{summary}

%prep
%setup -qn %{name}-%{version}
ls -d -1 logstash-filter-* 2>/dev/null > %{buildroot}logstash-plugin.conf || :
ls -d -1 logstash-input-*  2>/dev/null >> %{buildroot}logstash-plugin.conf || :
ls -d -1 logstash-output-*  2>/dev/null >> %{buildroot}logstash-plugin.conf || :

%build
export JAVA_HOME="/usr/share/logstash/jdk"

while IFS= read -r plugin; do
   pushd $plugin
     /usr/share/logstash/vendor/jruby/bin/jruby -S gem build $plugin.gemspec
   popd
   /usr/share/logstash/bin/logstash-plugin install $PWD/$plugin/*.gem
done < %{buildroot}logstash-plugin.conf

/usr/share/logstash/bin/logstash-plugin prepare-offline-pack --output %{name}-%{version}.zip $(cat %{buildroot}logstash-plugin.conf | tr '\n' ' ')

%install
mkdir -p %{buildroot}%{plugins_path}
mkdir -p %{buildroot}%{plugins_path}/scripts

install -m 644 -p %{name}-%{version}.zip %{buildroot}%{plugins_path}
install -m 755 -p %{_sourcedir}/scripts/* %{buildroot}%{plugins_path}/scripts/

%pre

%post
/usr/share/logstash/bin/logstash-plugin install --no-verify file://%{plugins_path}%{name}-%{version}.zip 2>&1 | tee -a /root/.install-logstash-plugins.log

%files
%defattr(0755,root,root)
%{plugins_path}
%defattr(0644,root,root)
%{plugins_path}%{name}-%{version}.zip

%changelog
* Mon Oct 20 2025 Luis Blanco <ljblanco@redborder.com>      - 
- added directory to store and run scripts for any logstash plugin
* Tue Oct 3 2023 David Vanhoucke <dvanhoucke@redborder.com> - 2.0.0-1
- update spec using logstash-plugin install
* Mon Nov 8 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.0-1
- Create and install logstash-plugins package
* Thu Oct 28 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.0-1
- first spec version