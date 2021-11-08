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

BuildRequires: yum, curl, grep, sudo

%description
%{summary}

%prep

%setup -qn %{name}-%{version}

%build
yum install logstash
yum install zip
#yum install gnupg2

%install
mkdir -p %{buildroot}%{plugins_path}

export JAVA_HOME="/usr/share/logstash/jdk"
export GEM_HOME="/opt/logstash/vendor/bundle/jruby/2.5.0/"
export LOGSTASH_HOME="/usr/share/logstash/"


#Install Dependencies
/usr/share/logstash/vendor/jruby/bin/jruby -S gem install logstash-core-plugin-api -v ">= 2.1.12, <= 2.99" -i /usr/share/logstash/vendor/bundle/jruby/2.5.0/
echo "logstash-core logstash-input-s3 logstash-input-file logstash-input-beats" | while read -r line;
do
   /usr/share/logstash/vendor/jruby/bin/jruby -S gem install $line -i /usr/share/logstash/vendor/bundle/jruby/2.5.0/
done

#Install Redborder Filters
ls | while read -r line;
do
   if [[ $line == *"logstash-"* ]]; then
     /usr/share/logstash/vendor/jruby/bin/jruby -S gem build $line/$line -v
     /usr/share/logstash/vendor/jruby/bin/jruby -S gem install $line*.gem -i /usr/share/logstash/vendor/bundle/jruby/2.5.0/
   fi
done


mkdir %{buildroot}%{plugins_path}gems
cp -r /usr/share/logstash/vendor/bundle/jruby/2.5.0/cache/ %{buildroot}%{plugins_path}gems

#cleaning cache install
rm -rf /usr/share/logstash/vendor/bundle/jruby/2.5.0/

mkdir %{buildroot}%{plugins_path}logstash
mkdir %{buildroot}%{plugins_path}logstash/dependencies

cd %{buildroot}%{plugins_path}
ls %{buildroot}%{plugins_path}gems/cache

#Creating the offline-pack manually
ls %{buildroot}%{plugins_path}gems/cache | while read -r line;
do
   if [[ $line != *"logstash-"* ]]; then
    mv %{buildroot}%{plugins_path}gems/cache/$line %{buildroot}%{plugins_path}logstash/dependencies
   else
     if [[ $line == *"logstash-filter"* || $line == *"logstash-input"* ]]; then
        mv %{buildroot}%{plugins_path}gems/cache/$line %{buildroot}%{plugins_path}logstash/
     else
        if [[ $line != *"logstash-core"* || $line != "gems-"* ]]; then
            mv %{buildroot}%{plugins_path}gems/cache/$line %{buildroot}%{plugins_path}logstash/dependencies
        fi
     fi
   fi
done

cd %{buildroot}%{plugins_path}
zip %{name}-%{version}.zip -r logstash/

#cleaning gems
rm -rf gems
rm -rf logstash

%pre

%post
su - -s /bin/bash -c 'source /etc/profile && rvm gemset use default'

if [ -f %{plugins_path}%{name}-%{version}.zip ]; then
    /usr/share/logstash/bin/logstash-plugin install --no-verify file://%{plugins_path}%{name}-%{version}.zip 2>&1 | tee -a /root/.install-redborder-boot.log
fi



%files
%defattr(0755,root,root)
%{plugins_path}

%doc

%changelog
* Mon Nov 8 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.1-1
- Create and install logstash-plugins package
* Thu Oct 28 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.0-1
- first spec version