%global cookbook_path /var/chef/cookbooks/logstash/
%global plugins_path /share/logstash-plugins/

Name: redborder-logstash-plugins
Version: %{__version}
Release: %{__release}%{?dist}
BuildArch: noarch
Summary: Logstash cookbook used to install redborder logstash plugins

License: AGPL 3.0
URL: https://github.com/redBorder/redborder-logstash-plugins
Source0: %{name}-%{version}.tar.gz

BuildRequires: yum

%description
%{summary}

%prep

%setup -qn %{name}-%{version}

%build
yum install java-1.8.0-openjdk.x86_64
yum install logstash
#yum install git

%install

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

%files
%defattr(0755,root,root)
%{plugins_path}

%doc

%changelog
* Thu Oct 28 2021 Javier Rodriguez <javiercrg@redborder.com> - 1.0.0-1
- first spec version