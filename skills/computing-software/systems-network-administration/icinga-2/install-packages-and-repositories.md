---
id: computing-software.systems-network-administration.icinga-2.install-packages-and-repositories
name: install-packages-and-repositories
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, installation, package-repository, systemd, icinga2-package, config-validation]
level: intro
status: docs-checked
description: "Install Icinga 2 from the official package repositories, enable the systemd service, and validate configuration with icinga2 daemon -C."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/02-installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# install packages and repositories
The docs recommend the official Icinga package repositories. Run the commands as root (for example after `sudo -i`) because pipes and nested commands are used.

Repository setup is per distribution: Debian and Ubuntu install an `icinga-archive-keyring` package, then write a `deb` and `deb-src` entry in `/etc/apt/sources.list.d/` that references the keyring with `signed-by`, then `apt update`. The RHEL, SLES and Amazon Linux repositories need a paid subscription. Sections also exist for RHEL, Fedora, SLES, openSUSE, Amazon Linux and Icinga for Windows.

Install the `icinga2` package:
- Debian/Ubuntu/Raspberry Pi OS: `apt install icinga2`
- RHEL 8 or later and Fedora: `dnf install icinga2`, then `systemctl enable icinga2` and `systemctl start icinga2`
- SLES/openSUSE: `zypper install icinga2`
- Amazon Linux: `yum install icinga2`, then enable and start

With SELinux enabled on RHEL, Fedora or Amazon Linux the package `icinga2-selinux` is also required.

The packages install the systemd unit files. If you are stuck with configuration errors, validate manually:
```
icinga2 daemon -C
```
If you hit fork errors on systemd distributions, see the troubleshooting chapter on check fork errors.

When upgrading an existing setup, follow the separate upgrade documentation.

Backup: include `/etc/icinga2` (configuration), `/var/lib/icinga2/ca` (master CA key pair), `/var/lib/icinga2/certs` (node certificates) and the runtime files in `/var/lib/icinga2`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/02-installation/.
Added: RHEL, SLES and Amazon Linux repositories need a paid subscription. No commands were run.
