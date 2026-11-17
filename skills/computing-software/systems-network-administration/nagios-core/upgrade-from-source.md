---
id: computing-software.systems-network-administration.nagios-core.upgrade-from-source
name: upgrade-from-source
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, upgrade, upgrading, source-install, make-install, nagcmd, lock-file]
level: practitioner
status: docs-checked
description: "Upgrade a source-built Nagios Core 4 in place: back up, configure with nagcmd, make install, verify, restart, plus the 4.3.0 and 4.3.4 config changes."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/upgrading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Nagios Core 4 from source

1. Back up the current install and all config files.
2. Become the nagios user (`su -l nagios`; on Debian/Ubuntu `sudo -s nagios`).
3. Remove old static front-end files: `/usr/local/nagios/share/{main,side,index}.html` (PHP versions replace them).
4. Download and extract the newest tarball, `cd` into it.
5. `./configure --with-command-group=nagcmd`
6. `make all`
7. `make install` - updates binaries, docs and web interface; it does NOT overwrite your existing config files.
8. `/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg` and fix every error.
9. Restart (`/etc/init.d/nagios restart` on Debian/Ubuntu, `/sbin/service nagios restart` elsewhere).

## Version-specific changes
- **4.2.4 or earlier to 4.3.0+:** update the Apache `nagios.conf`. Either merge the new sections from `sample-config/httpd.conf`, or back up `nagios.conf`, run `make install-webconf`, restart httpd.
- **4.3.3 or earlier to 4.3.4+:** run `make install-init` (review the old init script first if customised), find the new lock file path (`NagiosRunFile` in the init script, or `INIT_DIR` in the Makefile), and set `lock_file` in `nagios.cfg` to it.

## Packages
Use the package manager; repo versions are often much older than the source release. Back up first.

## Verify
Confirm with `nagios -v` and a restart; see `computing-software.systems-network-administration.nagios-core.verify-configuration`.

## Checked

2026-11-04. Read the Upgrading page: nagios user, removal of main/side/index.html, ./configure --with-command-group=nagcmd, make all, make install (config not overwritten), nagios -v, restart commands, the 4.2.4 to 4.3.0 nagios.conf change with make install-webconf, the 4.3.3 to 4.3.4 make install-init and lock_file change (NagiosRunFile, INIT_DIR), and the packaged-install note. Removed the unconfirmed Process Info version check.

Method: documentation only; no commands were run.
