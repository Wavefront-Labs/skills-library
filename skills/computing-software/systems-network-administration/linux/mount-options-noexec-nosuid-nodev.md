---
id: computing-software.systems-network-administration.linux.mount-options-noexec-nosuid-nodev
name: mount-options-noexec-nosuid-nodev
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystems, noexec, nosuid, nodev, mount-options, hardening, cis-benchmark, fstab, separate-partitions, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Harden mounts with nodev, nosuid and noexec: which paths get which flags (suggested baseline), applying them live with remount, what each really blocks, and what breaks."
sources:
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# noexec, nosuid, nodev

**Goal:** remove easy privilege-escalation and malware-execution paths from world-writable or
removable filesystems without breaking the system.

## 1. What each flag does
| Flag | Blocks | Doesn't block |
|---|---|---|
| `nodev` | device files on that fs being usable | — |
| `nosuid` | setuid/setgid bits and file capabilities taking effect | running normal binaries |
| `noexec` | direct execution of binaries and other executable files there | running a script by passing it to an interpreter that only reads it |
So `noexec` raises the bar for drive-by droppers, not a determined local user.

## 2. Where (suggested baseline; compare with your benchmark)
| Mount | nodev | nosuid | noexec |
|---|---|---|---|
| `/tmp`, `/var/tmp`, `/dev/shm` | ✓ | ✓ | ✓ |
| `/home` | ✓ | ✓ | (optional — breaks dev users) |
| `/var/log`, `/var/log/audit` | ✓ | ✓ | ✓ |
| `/var` | ✓ | ✓ | |
| removable media, NFS/CIFS client mounts | ✓ | ✓ | ✓ |
| `/boot`, `/boot/efi` | ✓ | ✓ | ✓ |
These need separate filesystems (partitions/LVs/tmpfs); a bind mount of a directory onto itself
with the flags is a workaround on existing systems: `/var/tmp /var/tmp none bind,nodev,nosuid,noexec 0 0`.

## 3. Apply
```bash
# fstab
UUID=…  /home  xfs  defaults,nodev,nosuid  0 0
tmpfs   /dev/shm  tmpfs  defaults,nodev,nosuid,noexec  0 0
mount -o remount,nodev,nosuid,noexec /tmp     # live
findmnt -no OPTIONS /tmp
findmnt -rn -o TARGET,OPTIONS | grep -v nosuid | grep -E '/tmp|/home|/var|/dev/shm'   # audit gaps
```
systemd units can add per-service restrictions without remounting globally:
`NoExecPaths=/tmp /var/tmp`, `ProtectHome=read-only`, `PrivateTmp=yes`.

## 4. What breaks with noexec
- Installers and package scripts that unpack to `/tmp` and execute from there: give them another
  temporary directory or remount temporarily (check each tool's documentation).
- Anything that runs programs from `/home` when home is noexec.

## Gotchas
- `nosuid` on `/` or `/usr` stops setuid programs such as `sudo` and `passwd` from working — never there.
- `user`/`users` mount options imply `noexec,nosuid,nodev` unless overridden later in the option list.
- Mount options are per mount point; a bind mount elsewhere without the flags bypasses them.

## Verify
- [ ] `cp /bin/true /tmp/t && /tmp/t` → "Permission denied".
- [ ] `findmnt` shows the flags on every path in your baseline after reboot.
- [ ] Package updates still complete (test a kernel/DKMS update).

## Checked
Checked 2026-10-26 against util-linux master mount(8) man page source and systemd.exec(5) source.
Confirmed: nodev, nosuid (set-user-ID, set-group-ID and file capabilities) and noexec (direct execution) definitions; `user`, `users`, `owner` and `group` imply nosuid and nodev (and noexec for user/users) unless overridden later; `mount -o bind,ro foo foo` and remount,bind changing nosuid/nodev/noexec per mount; `remount`; systemd NoExecPaths=, ProtectHome=read-only and PrivateTmp=.
The table is presented as a suggested baseline because the CIS benchmark is not freely readable.
Removed as unconfirmed: the `ld.so ./bin` example (the man page only says direct execution is refused), Debian apt TempDir, snap/flatpak, TMPDIR advice and EFI umask.
Method: documentation only; no commands were run.
