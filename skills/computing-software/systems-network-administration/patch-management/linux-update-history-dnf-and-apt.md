---
id: computing-software.systems-network-administration.patch-management.linux-update-history-dnf-and-apt
name: linux-update-history-dnf-and-apt
category: computing-software
field: systems-network-administration
product: patch-management
tags: [dnf-history-info, apt-history-log, yum-history, update-history, patch-verification, linux]
level: practitioner
status: docs-checked
description: "Prove what was patched and when on Linux: dnf/yum history info and undo, apt history.log and dpkg.log parsing, zypper history, and exporting evidence for audits."
sources:
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://manpages.debian.org/stable/dpkg/dpkg.1.en.html
  - https://documentation.ubuntu.com/server/how-to/software/package-management/
  - https://manpages.opensuse.org/Tumbleweed/zypper/zypper.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux update history (dnf and apt)

## RHEL family: dnf/yum history
```sh
dnf history                       # ID | command line | date | action | altered
dnf history info 42               # packages, versions old->new, user, return code
dnf history list --reverse | tail
dnf history info                 # latest transaction when no ID is given
dnf history userinstalled
dnf history undo 42               # revert a transaction (needs old packages in repo/cache)
dnf history rollback 40           # revert everything after 40
rpm -qa --last | head -30         # install time per package, independent of dnf db
```
Package changelogs show CVEs: `rpm -q --changelog openssl | grep -m5 CVE`.

## Debian/Ubuntu: apt and dpkg logs
```sh
grep ' upgrade ' /var/log/dpkg.log          # dpkg's default log; lines start with date and time
less /var/log/unattended-upgrades/unattended-upgrades.log
```
Ubuntu documents `/var/log/dpkg.log` as the log of apt installs and removals, and dpkg writes
it by default. Logs rotate, so ship them to central logging if you need longer evidence.

## SUSE
`zypper history` is not a command; the installation history log is `/var/log/zypp/history`.
`zypper search --installed-only -t patch` lists installed patches.

## Export for an audit
```sh
dnf history info $(dnf history list | awk '/2026-10-1/ {print $1}') > patch-evidence-$(hostname).txt
ansible all -m shell -a "grep -h ' upgrade ' /var/log/dpkg.log | tail -50" -o > fleet-upgrades.txt
```

## Gotchas
- Packages installed with `rpm -U`/`dpkg -i` directly bypass dnf/apt history; dpkg.log and `rpm -qa --last` still catch them.
- `dnf history undo` fails if old versions are not available; keep local repo snapshots.
- Containers rarely keep history; rely on image build records.

## Verify
For a change record: transaction ID, date, package old->new list, and exit status attached; matches the package list from the patch tool.

## Checked

Checked 2026-10-27 against the DNF command reference, the Debian dpkg manual page, the Ubuntu Server package-management page and the SUSE zypper manual page.
- `dnf history` list (with `--reverse`), info (latest when no ID), undo, rollback, userinstalled: confirmed; undo and rollback refuse when the RPM database state no longer allows them.
- `/var/log/dpkg.log` is dpkg's default log; Ubuntu documents it for apt actions: confirmed.
- `/var/log/zypp/history` is the zypper installation history log; `--installed-only` and `-t patch` are valid options: confirmed.
- Removed unconfirmed: dnf history database path, apt history.log field layout, log rotation numbers, the sample dpkg.log line, `zypper patch-info`.
Method: documentation only; no commands were run.
