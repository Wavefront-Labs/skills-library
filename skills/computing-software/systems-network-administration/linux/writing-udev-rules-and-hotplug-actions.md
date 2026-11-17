---
id: computing-software.systems-network-administration.linux.writing-udev-rules-and-hotplug-actions
name: writing-udev-rules-and-hotplug-actions
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, udev, udev-rule-writing, udev-match-keys, hotplug, udev-run, systemd-wants, device-permissions, symlink, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Write udev rules that match the right device and assign names, owners, modes and symlinks; run actions on hotplug safely via SYSTEMD_WANTS instead of long RUN scripts."
sources:
  - https://github.com/systemd/systemd/blob/main/man/udev.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd-udevd.service.xml
  - https://github.com/systemd/systemd/blob/main/man/udevadm.xml
  - https://github.com/systemd/systemd/blob/main/rules.d/60-persistent-storage.rules.in
  - https://github.com/systemd/systemd/blob/main/rules.d/70-uaccess.rules.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing udev rules and hotplug actions

**Goal:** a USB serial adapter always appears as `/dev/plc0` owned by group `dialout`, a disk
gets a stable alias, and plugging a backup drive starts a backup job.

## 1. Anatomy
One rule = one line of comma-separated keys. `==`/`!=` match, `=` assign, `+=` append, `:=`
assign final.
Match keys: `ACTION`, `SUBSYSTEM`, `KERNEL`, `DRIVER`, `ENV{KEY}`, `ATTR{x}` (this device),
and parent-search variants `SUBSYSTEMS`, `KERNELS`, `DRIVERS`, `ATTRS{x}`. Globs `*?[]` allowed.
Assign keys: `NAME` (network interfaces only; a device node cannot be renamed, only given extra symlinks), `SYMLINK+=`, `OWNER`, `GROUP`, `MODE`, `ENV{}`,
`TAG+=`, `RUN+=`, `ATTR{x}=` (write sysfs), `OPTIONS+=`.
Files: `/etc/udev/rules.d/NN-name.rules`, processed in lexical order; a same-named file in `/etc` replaces the one in `/usr/lib`.

## 2. Examples
```udev
# /etc/udev/rules.d/70-plc.rules — USB serial by vendor/product/serial
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="A9XYZ123", SYMLINK+="plc0", GROUP="dialout", MODE="0660"

# Disk alias by WWN
SUBSYSTEM=="block", ENV{DEVTYPE}=="disk", ENV{ID_WWN}=="0x5000c500a1b2c3d4", SYMLINK+="backupdisk"

# Give a group access to a USB device
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="6089", TAG+="uaccess", GROUP="plugdev", MODE="0660"
```
Get the values from `udevadm info -a` (see udevadm skill).

## 3. Hotplug actions
`RUN+=` programs run after all rules are processed, in systemd-udevd's sandbox: network access and mounting or unmounting
filesystems are not allowed, and forked or detached long-running processes are killed when event handling ends
(the event timeout is 180 seconds by default). So: **start a systemd unit instead** with the `SYSTEMD_WANTS` device property.
```udev
ACTION=="add", SUBSYSTEM=="block", ENV{ID_FS_UUID}=="1c2e…", TAG+="systemd", ENV{SYSTEMD_WANTS}+="usb-backup.service"
```
```ini
# /etc/systemd/system/usb-backup.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/usb-backup.sh
```
Keep `RUN+=` for tiny, quick actions (`RUN+="/usr/bin/logger plc attached"`), with absolute paths.

## 4. Apply and test
```bash
udevadm verify /etc/udev/rules.d/70-plc.rules     # check syntax and style
udevadm control --reload && udevadm trigger --action=add --subsystem-match=tty
udevadm test $(udevadm info -q path -n /dev/ttyUSB0)
```

## Gotchas
- Matching `KERNEL=="sdb"` is unstable — the kernel assigns names in discovery order; use serial/WWN/UUID.
- Mixing ATTRS from two different parent levels in one rule never matches.
- A rule numbered lower than the one that sets the property you match (e.g. `ID_FS_UUID` set by the 60-persistent-storage rules) cannot see it — number yours higher.
- `MODE="0666"` on devices is a security hole; prefer groups or the `uaccess` tag (see systemd's 70-uaccess rules).

## Verify
- [ ] Unplug/replug: `/dev/plc0` exists with the intended group/mode.
- [ ] Plugging the backup disk starts the unit (`journalctl -u usb-backup`); udev log shows no RUN timeouts.

## Checked

2026-10-26. systemd main (commit of 2026-10): udev(7) operators and keys, NAME for network interfaces only, symlink-only device naming, RUN restrictions (no network or mounting, long-running processes killed), SYSTEMD_WANTS recommendation, /etc priority and same-name replacement; systemd-udevd event timeout default 180 seconds; the 60-persistent-storage rules set ID_FS_UUID-derived links; 70-uaccess rules exist. Removed the systemd 254 gate and the mount-namespace explanation. Removed the I/O scheduler example and the device-unit Requires/After lines, which were not confirmed. Vendor and product IDs in examples are placeholders; test with udevadm test.

Method: documentation only; no commands were run.
