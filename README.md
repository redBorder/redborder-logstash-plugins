# redborder-logstash-plugins

General repository for custom filters in logstash that requires gem packaging.
This repository uses git submodules https://git-scm.com/docs/git-submodule

# Requirements

- Rocky Linux 9

# Setup

## Clone
- Clone project
```bash 
git https://github.com/redBorder/redborder-logstash-plugins
```

## Initialize submodules
```bash 
git submodule init
git submodule update --remote
```

## Add a new submodule from a repo
``` bash
git submodule add -- <repo_url>
```

## Build package

```bash
make rpm
```

# Development

## Move all gems

It is expected that you have created a new gem in the actual filter by installing from gemspec.
Read particular README.md for the filter you are currently interested. 
Then you can move them all at once by running...

```bash
scp_gems.sh -h <remote_host>
```

## Install a gem

Now the gems are in the target host, they can be installed one by one with ...-
```bash
/usr/share/logstash/bin/logstash-plugin install --no-verify --local </usr/share/logstash/vendor/bundle/jruby/2.5.0/cache/<the-gem-x.x.x.gem>>
```

## Check installed filters

```bash
/usr/share/logstash/bin/logstash-plugin list --verbose
```

## Create the rpm using **sudo make**
```bash
make rpm
```

# Delete

## Archived plugins

Some plugins can be archived because we are not currently using them in NG.
You will notice them because rather not making any change, the directory
has changes unstaged; where 'git status' command is requesting to add them.

Configuration of active filters is in .gitmodules

## Remove from a gem from host

```bash
/usr/share/logstash/bin/logstash-plugin remove logstash-filter-yara
```