---
id: computing-software.systems-network-administration.backup-and-recovery.bareos-webui-and-bacula-differences
name: bareos-webui-and-bacula-differences
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bareos-webui, bareos, bacula, backup-web-console, bareos-console-profile, bacula-fork]
level: practitioner
status: docs-checked
description: "Install and secure the Bareos WebUI with restricted console profiles, and know where Bareos came from: the Bacula 5.2 fork, config layout and Python plugin packages."
sources:
  - https://docs.bareos.org/IntroductionAndTutorial/InstallingBareosWebui.html
  - https://docs.bareos.org/IntroductionAndTutorial/WhatIsBareos.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bareos WebUI and Bareos vs Bacula

**Goal:** a working Bareos web console with least-privilege logins, and the facts to keep straight when moving between Bareos and Bacula.

## Requirements
- A working Bareos environment; the Director version and WebUI version must match.
- The WebUI can be installed on any host, not necessarily the Director's. The default install uses PHP-FPM with Apache having mod-rewrite and mod-fcgid enabled; PHP 7 or newer is recommended.
- WebUI is part of the Bareos project since 15.2.0. Restart Apache after installing the package.

## Install
```sh
apt-get install bareos-webui        # Debian/Ubuntu; yum/dnf/zypper on RHEL family and SUSE
```
The WebUI has no user management of its own: it logs in through named Console resources on the Director, each with its own password and profile. At least one is required.
```
*configure add console name=admin password=secret profile=webui-admin tlsenable=false
```
Or create `/etc/bareos/bareos-dir.d/console/admin.conf` with `Name`, `Password`, `Profile = "webui-admin"` and `TlsEnable = false`, then reload or restart the Director. Use your own name and a strong password. TLS-PSK is not available between the WebUI and the Director; to use TLS with certificates see the Bareos WebUI docs.

## Profiles
The package ships the `webui-admin` profile (copy it to the Director if the WebUI is on another host). It denies a few commands in its Command ACL (`.bvfs_clear_cache`, `.exit`, `.sql`, `configure`, `create`, `delete`, `purge`, `sqlquery`, `umount`, `unmount`) and allows everything else, with `*all*` for the Job, Schedule, Catalog, Pool, Storage, Client, FileSet, Where and Plugin Options ACLs. A Profile grants nothing by itself; only a Console that uses it does. For a lower-privilege user, define your own profile with narrower ACLs. Since Bareos 22 the profile includes `Plugin Options ACL = *all*` for plugin restores.

## Configuration files
- `/etc/bareos-webui/directors.ini`: one section per Director (`diraddress`, `dirport` default 9101, optional `catalog`, TLS settings). Several Directors can be listed.
- `/etc/bareos-webui/configuration.ini` (16.2.2 and later): session timeout, dashboard refresh, table settings, restore `filetree_refresh_timeout`.
- Run `.bvfs_update` frequently (for example a RunScript `Console = ".bvfs_update"` after the catalog backup); otherwise loading the restore file tree for large jobs can time out.
- Upgrading from Bareos 21 or lower to 22: the WebUI needs php-fpm instead of Apache mod-php.

## Bareos vs Bacula (what the pages state)
- Bareos is a fork of Bacula 5.2: in 2010 Bacula community developer Marco van Wieringen started collecting rejected or neglected community contributions in his own branch, which became Bareos. The Bareos documentation is likewise a fork of the Bacula documentation.
- Bareos config is split into per-resource files such as `/etc/bareos/bareos-dir.d/console/admin.conf` and `.../profile/webui-admin.conf`.
- Bareos packages include Python plugins for the File, Storage and Director daemons (for example LDAP, MariaDB backup, PostgreSQL, Proxmox VE, VMware), `bareos-storage-droplet` for object storage, and the Always Incremental scheme (since 16.2.4).
- Bareos 20.0.0 and later follow semantic versioning with exceptions; the Director and Storage Daemon stay backwards compatible with File Daemons of the previous two major releases.
- Bareos documents PostgreSQL as its catalog database.
The pages do not compare TLS defaults, Bacula web UIs or Bacula cloud drivers, so none are claimed here.

## Checked
2026-11-07. Read in full: Bareos InstallingBareosWebui (all sections including upgrade notes, nginx and php.ini). From WhatIsBareos I read the opening, History, Components, Catalog and version-number sections (lines 1-36) and searched the rest (package list) for plugin and storage package names; the remainder was not read line by line. Removed because the pages do not state them: the Bareos vs Bacula comparison table (TLS-PSK default between daemons, Baculum/BWeb, Bacula cloud driver, passive client, "protocol not interoperable"), the `webui-readonly` profile, "Profile ACLs default deny", the HTTPS reverse-proxy advice, and the invented Verify step. Corrected: install command uses `apt-get`; the WebUI-to-Director link has no TLS-PSK (reversing the old gotcha).
Method: documentation only; no commands were run.
