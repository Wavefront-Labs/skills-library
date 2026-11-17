---
id: computing-software.cybersecurity-defensive.system-hardening.suid-sgid-permission-audit
name: suid-sgid-permission-audit
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, suid-audit, sgid, file-permissions, world-writable, nosuid-mount, privilege-escalation]
level: practitioner
status: docs-checked
description: "Audit SUID and SGID binaries, world-writable files and unowned files on Linux, compare against a baseline, remove unnecessary bits and use nosuid mounts."
sources: ["https://github.com/gnu-mirror-unofficial/findutils/blob/master/find/find.1", "https://github.com/osquery/osquery/blob/master/specs/posix/suid_bin.table", "https://github.com/mkerrisk/man-pages/blob/master/man7/capabilities.7", "https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SUID/SGID and permission audit

**Goal:** only expected binaries carry SUID/SGID, no world-writable files without sticky protection, and changes are detected.

## Inventory
```
find / -xdev \( -perm -4000 -o -perm -2000 \) -type f -exec ls -l {} \; 2>/dev/null > /root/suid-$(date +%F).txt
find / -xdev -type f -perm -0002 2>/dev/null                 # world-writable files
find / -xdev -type d -perm -0002 ! -perm -1000 2>/dev/null   # world-writable dirs without sticky bit
find / -xdev \( -nouser -o -nogroup \) 2>/dev/null           # unowned files
```
Run per filesystem (`-xdev`) and include separate mounts (`/home`, `/var`).

## Assess
- Expected: only binaries that your distribution's packages install as setuid or setgid; keep the approved list with the baseline.
- Unexpected: interpreters, editors, `find`, `cp`, `bash`, custom scripts or binaries in `/home`, `/tmp`, `/opt`; treat as likely privilege escalation or a backdoor until explained.
- Verify package ownership with your package manager's file-ownership query and its package verification command.

## Remediate
- Remove unneeded bits: `chmod u-s /usr/bin/<tool>` (record it; a package update can reinstall the file's original mode, so enforce via config management).
- Mount options: `nosuid` makes the kernel ignore set-user-ID and set-group-ID bits (and file capabilities) on a filesystem (mount(8)); use `nosuid,nodev,noexec` on `/tmp`, `/var/tmp`, `/dev/shm`, removable media; `nosuid,nodev` on `/home`.
- Replace SUID needs with capabilities where possible: `setcap cap_net_bind_service=+ep /usr/local/bin/app`; audit with `getcap -r /` (see capabilities(7) for `setcap`/`getcap`).

## Ongoing
Diff today's list against the baseline in cron or via FIM, and alert on new entries. osquery's `suid_bin` table (`SELECT path FROM suid_bin;`) lists "suid binaries in common locations", so it complements rather than replaces a full `find` sweep.

## Verify
- [ ] Baseline file stored and diffed; new SUID files alert.
- [ ] `/tmp` and `/dev/shm` show `nosuid` in `findmnt`.

## Checked
Checked 2026-10-25 against the GNU findutils find(1) manual (gnu-mirror-unofficial/findutils mirror, last updated 2022), mount(8) (util-linux), capabilities(7) (man-pages mirror, 2021 snapshot) and the osquery `suid_bin` table definition. Confirmed: `-xdev`, `-perm -mode` (all listed bits set, so `-perm -4000` is setuid), `-nouser`/`-nogroup`, `-type`, `-exec`, `nosuid` semantics, and the `suid_bin` table's scope. Removed unconfirmed: the list of expected SUID binaries, the PwnKit reference, GTFOBins, rpm/dpkg/debsums command details. The CIS benchmark was not read.

Method: documentation only; no commands were run.
