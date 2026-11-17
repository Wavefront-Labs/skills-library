---
id: computing-software.digital-forensics-incident-response.evidence-handling.software-write-blocking-on-linux-and-windows
name: software-write-blocking-on-linux-and-windows
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [software-write-blocker, write-blocking, blockdev, linux-forensics, windows-forensics, dfir, blockdev-setro]
level: practitioner
status: docs-checked
description: "Apply software write blocking when no hardware blocker is available: blockdev and mount options on Linux, diskpart and automount on Windows, and the limits."
sources: ["https://man7.org/linux/man-pages/man8/blockdev.8.html", "https://man7.org/linux/man-pages/man8/mount.8.html", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/attributes-disk", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/automount"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Software write blocking on Linux and Windows

**Goal:** prevent the analysis host from writing to an attached evidence device when a hardware blocker is not possible (unusual interface, field triage).

## Linux
```bash
# Set the block device and its partitions read-only BEFORE any mount attempt
blockdev --setro /dev/sdb
blockdev --getro /dev/sdb   # prints 1 if read-only
# If mounting is needed for triage:
mount -o ro,noload /dev/sdb1 /mnt/evid
```
- blockdev(8): `--setro` sets the device read-only; access already mounted read-write is not affected, so run it first. `--getro` prints 1 if the device is read-only, 0 if not. Set it on each partition device too, and check each one.
- Disable desktop auto-mount so nothing mounts the device before you set it read-only.
- mount(8): `-o ro` alone may still write; ext3 and ext4 replay the journal if the filesystem is dirty. Use `ro,noload` for ext3/ext4, or set the block device read-only as above.

## Windows
- `diskpart`: select the evidence disk, then `attributes disk set readonly`.
- `automount disable` (a diskpart command) stops Windows automatically mounting new basic and dynamic volumes added to the system. The page notes that this can make failover cluster storage validation fail.
- Keep the evidence disk offline and image the physical device; do not rely on mounting it.

## Limits
Software blocking depends on the OS and drivers behaving; it is less defensible than a validated hardware blocker. Document the method and validate it.

## Verify
Hash the device before and after the session; test your method on a sacrificial drive (write attempt fails, hash unchanged) and record the test.

## Checked
Confirmed against the blockdev(8) page (`--setro`, `--getro`, mounted read-write caveat), the mount(8) page (ro still replays ext3/ext4 journals, `ro,noload`) and the Microsoft Learn pages for `attributes disk` (`readonly`) and `automount` (`disable` behaviour and cluster note). Removed claims the pages do not give: `systemctl mask udisks2`, the StorageDevicePolicies WriteProtect registry value, `mountvol /N` (the mountvol page has no such switch), the claim about forensic distros' defaults, and the NIST CFTT source (no claims relied on it).

Method: docs-only read of cited pages, 2026-11-09
