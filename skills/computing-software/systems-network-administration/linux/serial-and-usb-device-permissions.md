---
id: computing-software.systems-network-administration.linux.serial-and-usb-device-permissions
name: serial-and-usb-device-permissions
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dialout, serial-device-permissions, udev-rules, ttyusb, plugdev, uaccess, device-permissions]
level: practitioner
status: docs-checked
description: "Give users or services access to serial/USB devices: dialout/plugdev groups, udev MODE/GROUP/TAG+=uaccess rules, stable symlinks, and systemd SupplementaryGroups/DeviceAllow."
sources:
  - https://man7.org/linux/man-pages/man7/udev.7.html
  - https://www.freedesktop.org/software/systemd/man/latest/sd-login.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serial and USB device permissions

**Symptom:** `Permission denied: '/dev/ttyUSB0'`, or a USB programmer/dongle only works as root.

## Who owns it?
```bash
ls -l /dev/ttyUSB0 /dev/ttyACM0      # owner and group vary by distribution
udevadm info -q property -n /dev/ttyUSB0 | grep -E 'ID_VENDOR_ID|ID_MODEL_ID|ID_SERIAL'
```
## Group membership (serial ports)
`usermod -aG <group> alice` (the group that owns the device node; its name varies by distribution). Takes effect at the next login
(`newgrp dialout` for the current shell; check with `id`).

## udev rule for a specific device
`/etc/udev/rules.d/70-mydevices.rules`:
```
# serial adapter: fixed name, group-writable
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="A9XK3L2", SYMLINK+="ttyPLC", GROUP="dialout", MODE="0660"
# USB device (raw libusb access) for the logged-in desktop user
SUBSYSTEM=="usb", ATTR{idVendor}=="1d50", ATTR{idProduct}=="6089", TAG+="uaccess"
# for a service account
SUBSYSTEM=="usb", ATTR{idVendor}=="1d50", ATTR{idProduct}=="6089", GROUP="sdr", MODE="0660"
```
`udevadm control --reload && udevadm trigger --subsystem-match=tty --subsystem-match=usb`, then replug.
`uaccess` ties access to the device to an active seat (sd-login(3)), so it serves the local seated user, not remote logins.

## systemd services
```ini
[Service]
SupplementaryGroups=dialout
DeviceAllow=/dev/ttyPLC rw       # only needed when PrivateDevices=/DevicePolicy=closed restrict access
```
## Gotchas
- Other services (modem or braille daemons) can claim a new serial device; check what holds it before changing permissions.
- Containers need the device passed in by the runtime plus a matching group inside.

## Verify
- [ ] `ls -l /dev/ttyPLC` shows the symlink and group; the user opens it without sudo (`screen /dev/ttyPLC 115200`).

## Checked

Checked 2026-10-27 against systemd man pages (shutdown, systemctl, systemd-inhibit, udev, udevadm, sd-login, systemd.resource-control), linux-pam pam_nologin and pam_motd sources, efibootmgr man page source, current main, 2026-10-27. Confirmed: udev rule keys SUBSYSTEM, ATTRS, SYMLINK, GROUP, MODE and TAG uaccess semantics, udevadm info --query=property, udevadm trigger --subsystem-match, DeviceAllow and DevicePolicy in systemd.resource-control. Removed or softened: distribution group names, ModemManager ENV key and brltty remarks, container flag.

Method: documentation only; no commands were run.
