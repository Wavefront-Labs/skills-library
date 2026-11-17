---
id: computing-software.systems-network-administration.audiobookshelf.rhel-centos-package-install
name: rhel-centos-package-install
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [rhel, centos, dnf, rpm, systemd, amd64]
level: practitioner
status: docs-checked
description: "Install Audiobookshelf on Red Hat or CentOS Stream with the RPM repository package, set HOST and PORT, and enable the systemd service."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/linux/4.linux-install-rpm.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only **amd64** and **Red Hat / CentOS Stream** variants are supported. Activate the repository and install:

```bash
dnf install -y "https://github.com/lkiesow/audiobookshelf-rpm/raw/el$(rpm -E %rhel)/audiobookshelf-repository-1-1.el$(rpm -E %rhel).noarch.rpm"
dnf install audiobookshelf
```

Configure in `/etc/default/audiobookshelf` with the same options you would pass to Docker:

```bash
METADATA_PATH=/var/lib/audiobookshelf/metadata
CONFIG_PATH=/var/lib/audiobookshelf/config
PORT=13378
HOST=127.0.0.1
```

By default it listens on localhost only, which is enough behind a reverse proxy. To listen on all interfaces set `HOST=0.0.0.0`.

Start and enable at boot, then check status:

```bash
systemctl start audiobookshelf.service
systemctl enable audiobookshelf.service
systemctl status audiobookshelf.service
```

Backups from other install methods cannot be loaded after installation without losing progress.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: RHEL, CentOS install page.

Method: documentation only; no commands were run.
