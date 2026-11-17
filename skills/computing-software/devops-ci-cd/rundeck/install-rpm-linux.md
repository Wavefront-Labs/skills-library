---
id: computing-software.devops-ci-cd.rundeck.install-rpm-linux
name: install-rpm-linux
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, yum-install, rpm-package, rundeck-group, port-4440]
level: intro
status: docs-checked
description: "Install Rundeck Community on Red Hat, Amazon or Oracle Linux with the yum repo or an rpm file, start rundeckd and log in for the first time."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/install/linux-rpm.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quick install of the yum repo and package (use `rundeckpro` in place of `rundeck` for Enterprise):

```bash
curl https://raw.githubusercontent.com/rundeck/packaging/main/scripts/rpm-setup.sh 2> /dev/null | sudo bash -s rundeck
```

Manual repo: put this in `/etc/yum.repos.d/rundeck.repo`, replacing existing entries. The page also lists a second `gpgkey` URL (a build key under `docs.rundeck.com/keys/`); copy the full file from the page.

```properties
[rundeck]
name=rundeck
baseurl=https://packages.rundeck.com/pagerduty/rundeck/rpm_any/rpm_any/$basearch
repo_gpgcheck=1
gpgcheck=1
enabled=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
```

Upgrade later with `sudo yum update rundeck`. To install a downloaded file use `sudo rpm -i <file>.rpm`.

Start and verify:

```bash
sudo service rundeckd start
tail -f /var/log/rundeck/service.log
```

Ready when the log shows `Grails application running at http://localhost:4440`. Log in as `admin` / `admin`.

The RPM creates a unix group named `rundeck`; check with `groups rundeck`.

Gotcha: for Enterprise, remove `bintray-rundeckpro-rpm.repo` if it exists.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Installing on Red Hat, Amazon or Oracle Linux: rpm-setup.sh quick install with rundeck or rundeckpro, /etc/yum.repos.d/rundeck.repo entries, yum update, rpm -i, service rundeckd start, service.log, Grails ready line, admin/admin login, the rundeck unix group, and removal of bintray-rundeckpro-rpm.repo for Enterprise. Nothing removed.

Method: documentation only; no commands were run.
