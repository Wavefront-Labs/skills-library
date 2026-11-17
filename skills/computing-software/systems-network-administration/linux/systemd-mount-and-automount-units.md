---
id: computing-software.systems-network-administration.linux.systemd-mount-and-automount-units
name: systemd-mount-and-automount-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, mount-unit, systemd-mount, automount, fstab-generator, x-systemd, nofail, network-mounts, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Mount filesystems the systemd way: .mount/.automount units and naming, fstab x-systemd options, nofail and timeouts for network mounts, and ordering services after mounts."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.automount.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-fstab-generator.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-mount.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd mount and automount units

**Goal:** mounts that don't hang boot when storage is missing, mount on first access, and that
services can depend on.

## 1. fstab is already systemd
`systemd-fstab-generator` turns each fstab line into `/run/systemd/generator/<path>.mount`.
systemd converts fstab entries to mount units at boot and when `systemctl daemon-reload` runs, so reload after editing. Useful fstab options:
```
UUID=…  /data  xfs  defaults,nofail,x-systemd.device-timeout=10s  0 0
nas:/export  /mnt/nas  nfs  _netdev,nofail,x-systemd.automount,x-systemd.idle-timeout=10min,x-systemd.mount-timeout=30s  0 0
/srv/a  /var/lib/a  none  bind,x-systemd.requires-mounts-for=/srv  0 0
```
`nofail`: the mount is not a requirement of `local-fs.target`, so boot continues without it. `_netdev` makes systemd treat the mount as a network mount. `x-systemd.automount`: mount on first access.

## 2. Native units
Unit name must be the escaped mount path: `/srv/backup` → `srv-backup.mount`
(`systemd-escape -p --suffix=mount /srv/backup`).
```ini
# /etc/systemd/system/srv-backup.mount
[Unit]
Description=Backup volume
[Mount]
What=nas:/export/backup
Where=/srv/backup
Type=nfs
Options=_netdev
TimeoutSec=30
[Install]
WantedBy=multi-user.target
```
```ini
# /etc/systemd/system/srv-backup.automount
[Automount]
Where=/srv/backup
TimeoutIdleSec=600
[Install]
WantedBy=multi-user.target
```
Enable the **automount** (not the mount) for on-demand: `systemctl enable --now srv-backup.automount`.

## 3. Ordering services after mounts
```ini
[Unit]
RequiresMountsFor=/srv/backup      # adds Requires+After on the mount units for that path
```

## 4. Ad hoc
```bash
systemd-mount /dev/sdc1 /mnt/usb           # transient mount unit
systemd-mount --automount=yes nas:/x /mnt/x
systemd-umount /mnt/usb
systemctl list-units -t mount,automount
```

## Gotchas
- The mount unit must be named after its mount point (`Where=`); a mismatch is an error.
- A mount without `nofail` is a requirement of `local-fs.target`, so a failing entry can block boot.

## Verify
- [ ] `systemctl status srv-backup.mount` active; `findmnt /srv/backup` shows options.
- [ ] Boot with the device/server unavailable: system reaches multi-user.target, mount just fails/waits.
- [ ] `systemd-analyze verify /etc/systemd/system/srv-backup.mount` passes.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: fstab options `nofail`, `_netdev`, `x-systemd.automount`, `x-systemd.device-timeout=`, `x-systemd.idle-timeout=`, `x-systemd.requires-mounts-for=`; fstab conversion on daemon-reload; mount units named after the mount point; network mounts automatically get network-online dependencies; `TimeoutSec=`, `TimeoutIdleSec=`, `RequiresMountsFor=`; `systemd-mount --automount=` and `systemd-escape --path --suffix=`. Removed the CIFS example options, the emergency-mode claim and two gotchas that no documentation covers.

Method: documentation only; no commands were run.
