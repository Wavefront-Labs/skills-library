---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usb-device-history-on-linux-and-macos
name: usb-device-history-on-linux-and-macos
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [linux-usb-history, usb-forensics, linux-forensics, macos-forensics, removable-media, dfir]
level: practitioner
status: draft
description: "Reconstruct USB device history on Linux (kernel logs, journald, udev) and macOS (unified logs, IORegistry, fsevents) including serials and mount points."
sources: ["https://www.kernel.org/doc/html/latest/driver-api/usb/index.html", "https://man7.org/linux/man-pages/man1/journalctl.1.html", "https://developer.apple.com/documentation/os/logging"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB device history on Linux and macOS

**Goal:** same questions as on Windows (which device, when, who, what files) but different sources.

## Linux
- **Kernel messages** in journald / `/var/log/kern.log`, `syslog`, `messages`:
  `usb 1-1: New USB device found, idVendor=0781, idProduct=5581`, `SerialNumber: 4C53...`,
  `sd 6:0:0:0: [sdb] Attached SCSI removable disk`, then mount messages.
```bash
journalctl -k --since "2026-10-01" | grep -Ei "usb .*(new|serial|disconnect)|attached scsi"
journalctl --list-boots   # journal persists across boots only if /var/log/journal exists
zgrep -h "SerialNumber" /var/log/kern.log* /var/log/syslog*
```
- **udisks2 / desktop auto-mount** logs: `udisksd[...]: Mounted /dev/sdb1 at /media/<user>/LABEL` - ties to a user.
- `/etc/fstab`, `/run/media`, `~/.local/share/recently-used.xbel` (GNOME recent files incl. removable paths), shell history with `cp`/`rsync` to `/media/...`.
- usbguard logs if deployed.

## macOS
- **Unified logs**:
```bash
log show --predicate 'subsystem == "com.apple.iokit" OR process == "diskarbitrationd"' --start "2026-10-01" --info
log show --predicate 'eventMessage CONTAINS[c] "USBMSC"' --last 30d
```
- `diskarbitrationd` messages show mount of `/Volumes/<LABEL>` with BSD names.
- FSEvents records file activity on removable volumes (each volume has its own `.fseventsd`
  on the device itself - examine the USB drive too).
- `system_profiler SPUSBDataType` (live) gives currently attached devices with serials.

## Gotchas
- Log retention on both platforms is days to weeks; collect early.
- Serial numbers can be absent/duplicated on cheap devices; combine with vendor/product IDs and capacity.

## Verify
Device sessions are tied to a user via mount logs and to file activity via shell history, recent files or FSEvents.
