# redborder-logstash-plugins

rpm to install RedBorder Logstash Plugins in RedBorder NG.
This repository uses git submodules https://git-scm.com/docs/git-submodule

### Platforms

- Rocky Linux 9

### Steps
- Clone project

- Initialize submodules
```
git submodule init
git submodule update
```

- Add a new submodule from a repo
``` bash
git submodule add -- <repo_url>
```

- Update submodules to latests versions
```
git submodule update --remote
```

- Create the rpm using **sudo make**

## Archived plugins

Some plugins can be archived because we are not currently using them in NG.
You will notice them because rather not making any change, the directory
has changes unstaged; where 'git status' command is requesting to add them.

Configuration of active filters is in .gitmodules
