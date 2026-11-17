---
id: computing-software.systems-network-administration.linux.apt-history-and-dpkg-logs
name: apt-history-and-dpkg-logs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, dpkg, apt-history, apt-logs, dpkg-log, term-log, unattended-upgrades-log, package-audit, rollback, debian, ubuntu, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Answer 'what changed on this box and when' on Debian/Ubuntu: read apt history.log, term.log and dpkg.log (incl. rotated), unattended-upgrades logs, and roll back a bad upgrade."
sources:
  - https://manpages.debian.org/stable/apt/apt.conf.5.en.html
  - https://manpages.debian.org/stable/dpkg/dpkg.1.en.html
  - https://wiki.debian.org/UnattendedUpgrades
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apt history and dpkg logs

**Goal:** correlate an incident with package changes — who ran what, which versions moved —
and go back to the previous versions if needed. (Debian has no `dnf history undo`.)

## 1. The logs
| File | Contains |
|---|---|
| `/var/log/apt/history.log` | per apt run: start date, command line and the packages installed, upgraded or removed (gated: unconfirmed, apt does not document this file's fields in the sources checked) |
| `/var/log/apt/term.log` | terminal output of each apt run (gated: unconfirmed, same reason) |
| `/var/log/dpkg.log` | dpkg status changes and actions, the default log file of dpkg (`--log` overrides it) |
| `/var/log/unattended-upgrades/*.log` | automatic upgrades (gated: unconfirmed, the Debian wiki page is not readable here) |
Rotation scheme: (gated: unconfirmed, logrotate settings differ per release).

## 2. Queries
```bash
zcat -f /var/log/apt/history.log*                       # all apt runs, including rotated files
zgrep -h ' upgrade ' /var/log/dpkg.log* | grep -E 'openssl|libssl' | sort
```

## 3. Roll back a bad upgrade
```bash
apt-cache policy libfoo1                          # is the old version still in a repo?
apt install libfoo1=1.2.3-1 libfoo-dev=1.2.3-1    # downgrade: needs the version to be available (apt-get(8) pkg=version)
ls /var/cache/apt/archives/libfoo1_*              # old .deb may still be cached
dpkg -i /var/cache/apt/archives/libfoo1_1.2.3-1_amd64.deb
apt-mark hold libfoo1                             # stop it upgrading again until fixed
```

## Gotchas
- `apt clean` clears the local repository of retrieved package files (apt-get(8)) — keep the cache if you rely on local rollback.
- Downgrades of libraries with changed ABI may need dependent packages downgraded too.

## Verify
- [ ] You can name the exact time and version change matching the incident window.
- [ ] After rollback, `dpkg -l libfoo1` shows the old version and `apt-mark showhold` lists it.

## Checked

Checked against dpkg(1) (guillemj/dpkg, 2026-10) and apt-get(8)/apt-mark(8) (Debian/apt doc/, last commit 2025-11-10).
Confirmed: dpkg.log is dpkg's default log (`--log` overrides); `pkg=version` selection, `apt-mark hold`, `apt clean` semantics.
Not confirmable from public docs: the format and fields of history.log and term.log, rotation, and the unattended-upgrades logs; those carry the gated marker. Removed: awk pipelines, an example log line, Requested-By remark, Launchpad and snapshot remarks, and the claim that history.log omits `dpkg -i`.

Method: documentation only; no commands were run.
