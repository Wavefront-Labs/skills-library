---
id: computing-software.systems-network-administration.linux.rebuild-a-corrupt-rpm-database
name: rebuild-a-corrupt-rpm-database
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rpm, rpmdb-rebuild, rpm-rebuilddb, rpmdb-corruption, dnf, berkeleydb, sqlite]
level: advanced
status: docs-checked
description: "Fix rpm/dnf hangs and 'rpmdb open failed' errors: stale locks, rpm --rebuilddb, verifying with rpm -qa and rpm --verifydb, backups, and BDB vs sqlite backends."
sources:
  - https://access.redhat.com/solutions/6903
  - https://fedoraproject.org/wiki/Changes/Sqlite_Rpmdb
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Repairing a corrupt RPM database

**Symptoms:** rpm cannot open or read its database, or `rpm -qa` / `dnf` hang.

## 1. Make sure nothing is running
```bash
ps aux | grep -E '[r]pm|[d]nf|[y]um|[P]ackageKit'
```

## 2. Back up
Copy the database directory (`/var/lib/rpm` or the location your rpm build uses) before changing anything:
```bash
tar czf /root/rpmdb-$(date +%F).tgz /var/lib/rpm
```
## 3. Rebuild
```bash
rpmdb --rebuilddb                   # rebuild from installed package headers; discards unreadable headers and compacts
rpmdb --verifydb                    # low-level integrity check (rarely useful, per rpmdb(8))
rpm --verify -a                     # the more meaningful system health check
rpm -qa | wc -l                     # compare with a known count
dnf clean all && dnf makecache
```
`rpm --rebuilddb` is the same operation (rpm(8) refers to rpmdb(8)); it can also convert between rpmdb formats.

## 4. If packages are missing from the database
Files are on disk but rpm forgot them: restore the backup from step 2 if it predates the damage, or
re-register each package with `rpm -ivh --justdb pkg.rpm` (`--justdb` updates only the database).

## Prevent
- Do not kill dnf during transactions; use `dnf history undo` instead.

## Verify
- [ ] `rpm -qa` returns promptly with the expected count; `rpm --verify -a` shows only expected differences.

## Checked

Checked against rpmdb(8) and rpm(8) (rpm-software-management/rpm docs/man, last push 2026-10-22) and dnf4 command_ref.rst.
Confirmed: `rpmdb --rebuilddb` (rebuild from headers, discard unreadable headers, compact, convert formats), `--verifydb` and its caveat, `--initdb`, `rpm --justdb`, `dnf history undo`.
Removed as unconfirmed: the BDB error strings, the Berkeley DB `__db.*` file deletion, mapping of database formats to RHEL/Fedora releases, the rpm 4.16 version gate, systemctl and PackageKit commands, `/var/log/dnf.rpm.log` and the disk-full cause.

Method: documentation only; no commands were run.
