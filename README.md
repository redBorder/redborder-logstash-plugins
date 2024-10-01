# redborder-logstash-plugins

rpm to install RedBorder Logstash Plugins in RedBorder NG.

### Platforms

- Rocky Linux 9

### Steps
- Clone project

- Initialize submodules
```
git submodule init
git submodule update
```

- Update submodules to latests versions
```
git submodule update --remote
```

- Create the rpm using **sudo make**
