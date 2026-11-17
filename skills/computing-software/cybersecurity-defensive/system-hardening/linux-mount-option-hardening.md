---
id: computing-software.cybersecurity-defensive.system-hardening.linux-mount-option-hardening
name: linux-mount-option-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, mount-hardening, noexec, nosuid, nodev, tmp-partition, dev-shm, fstab, cis-benchmark]
level: practitioner
status: docs-checked
description: "Apply nodev, nosuid and noexec to /tmp, /dev/shm, /var/tmp and removable media per CIS: partitions or tmpfs, fstab and systemd units, and what noexec does not stop."
sources: ["https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc", "https://github.com/systemd/systemd/blob/main/units/tmp.mount"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux mount option hardening

World-writable locations (`/tmp`, `/var/tmp`, `/dev/shm`) are where attackers drop and run payloads and
where SUID tricks and device files get abused. Mount options remove those capabilities.

## Options
- `nodev`: do not interpret character or block special devices on the filesystem.
- `nosuid`: do not honour set-user-ID and set-group-ID bits or file capabilities when executing programs from this filesystem.
- `noexec`: do not permit direct execution of any binaries on the mounted filesystem.

## Typical targets (adapt to the benchmark you follow)
| Mount | Options |
|---|---|
| `/tmp` (separate partition or tmpfs) | nodev, nosuid, noexec |
| `/dev/shm` | nodev, nosuid, noexec |
| `/var/tmp` (separate or bind to /tmp) | nodev, nosuid, noexec |
| `/home` | nodev (nosuid often too) |
| `/var/log`, `/var/log/audit` (separate partitions) | nodev, nosuid, noexec |
| removable media | nodev, nosuid, noexec |

## Implement
fstab:
```
tmpfs  /tmp      tmpfs  defaults,rw,nosuid,nodev,noexec,relatime,size=2G  0 0
tmpfs  /dev/shm  tmpfs  defaults,rw,nosuid,nodev,noexec,relatime        0 0
/tmp   /var/tmp  none   bind                                             0 0
```
Or systemd: the upstream `tmp.mount` unit mounts a tmpfs on `/tmp` with `Options=mode=1777,strictatime,nosuid,nodev,size=50%,nr_inodes=1m,...`; it already sets `nosuid` and `nodev`, so an override (`systemctl edit tmp.mount`) only needs to add `noexec` (an override must restate the full `Options=` line).
Apply without reboot: `mount -o remount,nosuid,nodev,noexec /dev/shm`; check with `findmnt -no OPTIONS /tmp`.
Separate partitions for `/var`, `/var/log`, `/var/log/audit`, `/home` are decided at install time (LVM helps).

## Application compatibility
Some installers and tools execute from `/tmp`.
Test; point such apps to a dedicated `TMPDIR` with exec allowed rather than relaxing `/tmp`.

## Limits
`noexec` does not stop interpreters: `bash /tmp/x.sh`, `python3 /tmp/x.py`, or `ld.so /tmp/bin` still run.
It raises the bar against dropped binaries; combine with application control, auditd rules on
execution from `/tmp`, and EDR.

## Verify
`findmnt -no OPTIONS /tmp /dev/shm /var/tmp` lists nodev,nosuid,noexec; copying `/bin/true` to `/tmp` and
running `/tmp/true` fails with "Permission denied".

## Checked
Checked 2026-10-25 against mount(8) (util-linux/util-linux, `sys-utils/mount.8.adoc`) and the upstream systemd `units/tmp.mount` file (systemd/systemd, 2026-10). Confirmed: the meaning of `nodev`, `nosuid` and `noexec`, remount with a changed option set, and that the shipped tmp.mount already sets `nosuid,nodev` (so only `noexec` is missing). Removed unconfirmed apt-hook, fapolicyd and scanner claims; the CIS table is labelled as typical targets and the benchmark text (paywalled) was not read.

Method: documentation only; no commands were run.
