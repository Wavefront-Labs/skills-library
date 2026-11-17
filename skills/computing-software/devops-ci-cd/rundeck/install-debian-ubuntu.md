---
id: computing-software.devops-ci-cd.rundeck.install-debian-ubuntu
name: install-debian-ubuntu
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, apt-install, deb-package, rundeckd, port-4440]
level: intro
status: docs-checked
description: "Install Rundeck Community on Ubuntu or Debian from the apt repository or a deb file, start the service and confirm it is up on port 4440."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/install/linux-deb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install a Java runtime first (the page uses `openjdk-17-jre-headless`):

```bash
sudo apt-get install openjdk-17-jre-headless
```

Quick install of the repo and Community package (use `rundeckpro` instead of `rundeck` for Enterprise):

```bash
curl https://raw.githubusercontent.com/rundeck/packaging/main/scripts/deb-setup.sh 2> /dev/null | sudo bash -s rundeck
```

Manual route: import the signing key from `https://packages.rundeck.com/pagerduty/rundeck/gpgkey`, put these lines in `/etc/apt/sources.list.d/rundeck.list` (replacing existing entries), then `apt-get update` and `apt-get install rundeck`:

```
deb https://packages.rundeck.com/pagerduty/rundeck/any/ any main
deb-src https://packages.rundeck.com/pagerduty/rundeck/any/ any main
```

Or download the deb from the download page and run `sudo dpkg -i` on it.

Start and verify:

```bash
sudo systemctl daemon-reload
sudo service rundeckd start
tail -f /var/log/rundeck/service.log
```

Ready when the log shows `Grails application running at http://localhost:4440 in environment: production`. Browse to port 4440 and log in as `admin` / `admin`.

Gotcha: for a clean Enterprise reinstall, remove the old `rundeckpro-enterprise` package with `dpkg --purge` first.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Installing on Ubuntu or Debian: openjdk-17-jre-headless, deb-setup.sh quick install with rundeck or rundeckpro, the apt source lines and signing key URL, dpkg -i route, systemctl daemon-reload and service rundeckd start, service.log path and the Grails ready line, admin/admin login, and the dpkg --purge clean reinstall for rundeckpro-enterprise. Nothing removed.

Method: documentation only; no commands were run.
