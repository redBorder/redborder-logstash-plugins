%global cookbook_path /var/chef/cookbooks/logstash/
%global plugins_path /share/logstash-plugins/

Name: redborder-logstash-plugins
Version: %{__version}
Release: %{__release}%{?dist}
BuildArch: noarch
Summary: Logstash cookbook used to install redborder logstash plugins

License: AGPL 3.0
URL: https://github.com/redBorder/redborder-logstash-plugins
Source0: %{name}-%{version}.tar

BuildRequires: yum

%description
%{summary}

%prep

%setup -qn %{name}-%{version}

%build
yum install java-1.8.0-openjdk.x86_64
yum install logstash
#yum install git
#yum install unzip

%install
mkdir -p %{buildroot}%{plugins_path}

ls | while read -r line;
do
   if [[ $line == *"logstash-"* ]]; then
     /usr/share/logstash/vendor/jruby/bin/jruby -S gem build $line/$line -v
     /usr/share/logstash/bin/logstash-plugin install $line*.gem
   fi
done

#/usr/share/logstash/bin/logstash-plugin prepare-offline-pack --output $RPM_SOURCE_DIR/%{name}-%{version}.zip --overwrite $(git config --file .gitmodules --get-regexp path | awk '{ print $2 }')
/usr/share/logstash/bin/logstash-plugin prepare-offline-pack --output $RPM_SOURCE_DIR/%{name}-%{version}.zip logstash-input-redfish logstash-input-file logstash-filter-bulkstats logstash-input-s3 logstash-input-beats logstash-filter-netflowenrich logstash-filter-macvendorsenrich logstash-filter-darklist logstash-filter-location logstash-filter-mobility logstash-input-rbwindow logstash-filter-macscrambling logstash-filter-apstate logstash-filter-radius logstash-filter-meraki logstash-filter-nmsp logstash-filter-intrusion logstash-filter-mongocve


cp -f $RPM_SOURCE_DIR/%{name}-%{version}.zip %{buildroot}%{plugins_path}
#unzip $RPM_SOURCE_DIR/%{name}-%{version}.zip
#ls -la logstash/dependencies/
#ls -la /usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/

%pre

%post
case "$1" in
  1)
    # This is an initial install.
    :
  ;;
  2)
    # This is an upgrade.
    su - -s /bin/bash -c 'source /etc/profile && rvm gemset use default && env knife cookbook upload logstash'
  ;;
esac
if [ -f %{plugins_path}%{name}-%{version}.zip ]; then
    /usr/share/logstash/bin/logstash-plugin install --no-verify file://%{plugins_path}%{name}-%{version}.zip 2>&1 | tee -a /root/.install-redborder-boot.log
fi


%files
%defattr(0755,root,root)
%{plugins_path}

%doc

%changelog
* Thu Oct 28 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.0-1
- first spec version