---
id: computing-software.systems-network-administration.patch-management.aide-file-integrity-monitoring
name: aide-file-integrity-monitoring
category: computing-software
field: systems-network-administration
product: patch-management
tags: [aide, file-integrity-monitoring, drift-detection, configuration-baseline, unauthorised-change, linux]
level: practitioner
status: docs-checked
description: "Set up AIDE file integrity monitoring on Linux: database init, rules, daily checks, updating the baseline after patching, protecting the database, and reducing noise."
sources:
  - https://aide.github.io/
  - https://github.com/aide/aide/blob/master/doc/aide.conf.5
  - https://github.com/aide/aide/blob/master/doc/aide.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AIDE file integrity monitoring

AIDE (Advanced Intrusion Detection Environment) records hashes and attributes of files and
reports differences. File integrity monitoring is a common compliance control; check the current text of your standard for exact requirements.

## Install and initialise
```sh
dnf install aide        # or apt install aide aide-common
aide --init             # Debian: aideinit
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
```
Config and database paths (`database_in`, `database_out`) come from your distribution's build and config file; `aide --version` shows the compiled-in defaults. Adjust the `mv` commands to match.

## Rules (examples)
```
# groups
NORMAL = p+i+n+u+g+s+m+c+sha512
DIR = p+i+n+u+g
LOG = p+u+g+n+growing+s  # growing files: size may grow only (the old `S` attribute is deprecated since AIDE 0.18)
/etc       NORMAL
/usr/bin   NORMAL
/usr/sbin  NORMAL
/boot      NORMAL
/var/log   LOG
!/var/log/journal
!/etc/mtab
```

## Run daily
```sh
aide --check            # exit status: 0 = no differences; 1 new, 2 removed, 4 changed files are added together
```
Check whether your distribution package installs a scheduled job; if not, add a systemd timer or cron job that
mails or ships the report to SIEM.

## After patching (the step people forget)
Patches legitimately change hundreds of files. After a verified patch run:
```sh
aide --update && mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
```
Better: compare the change list with `rpm -Va` / package manifests first, so you don't bless
a malicious change that happened alongside patching.

## Protect the database
An attacker with root can update the DB. Copy `aide.db.gz` and the config off-host (read-only
location) after each update, or check against an off-host copy; record its hash.

## Reduce noise
Exclude volatile paths (`/var/lib/...` caches, `/tmp`, container storage), use `LOG` rules for
growing files, and treat repeated expected changes by fixing rules rather than ignoring
reports.

## Verify
Modify a test file in `/etc`: next check reports it; after a patch cycle, the baseline is
updated and checks return clean.

## Checked
Date: 2026-10-27. Documentation: AIDE project site and the aide.1 and aide.conf.5 manual pages in the aide/aide repository (--init, --check, --update, database_in/database_out, exit status bits 1, 2, 4, negative rule syntax, group `>` for growing files, `S` attribute deprecated since v0.18 in favour of growing+s, sha512 attribute). Corrected the deprecated `S` attribute; removed unconfirmed per-distribution timer and compliance-clause claims.
Method: documentation only; no commands were run.
