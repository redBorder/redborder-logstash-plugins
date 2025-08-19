# redborder-logstash-plugins

This repository serves as a container for multiple RedBorder Logstash plugins, managing them as submodules to create a unified RPM package for RedBorder NG platform.

## Purpose

- Centralizes management of multiple Logstash plugin repositories
- Provides a single build point for all plugins
- Ensures consistent versioning across all plugins
- Simplifies deployment through a unified RPM package

## Supported Platforms

- Rocky Linux 9.6

## Repository Structure

This repository contains multiple Logstash plugins as Git submodules. Each submodule is an independent repository containing a specific Logstash plugin.

## Clone the Repository

```bash
git clone https://github.com/redBorder/redborder-logstash-plugins.git
cd redborder-logstash-plugins
```

## Initialize and Update Submodules

- Initialize submodules
```bash 
git submodule init
```

- Update submodules to latests versions
``` bash
git submodule update --remote
```

To update a specific submodule:
```bash
cd [submodule_directory]
git checkout master
git pull
cd ..
git add [submodule_directory]
git commit -m "Update submodule to latest version"
```

## Building

### Create general RPM Package
```bash
sudo make
```

This should:
1. Build all individual plugins
2. Package them into a single RPM
3. Create installation files and dependencies

## Maintenance

### Adding a New Plugin
```bash
git submodule add [repository_url] [directory_name]
git commit -m "Add new plugin submodule"
```

### Removing a Plugin
```bash
git submodule deinit [directory_name]
git rm [directory_name]
git commit -m "Remove plugin submodule"
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
