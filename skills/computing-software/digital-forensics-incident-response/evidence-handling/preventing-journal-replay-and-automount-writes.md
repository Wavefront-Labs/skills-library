---
id: computing-software.digital-forensics-incident-response.evidence-handling.preventing-journal-replay-and-automount-writes
name: preventing-journal-replay-and-automount-writes
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [journal-replay, write-blocking, software-write-blocker, evidence-integrity, dfir]
level: advanced
status: docs-checked
description: "Stop Linux replaying an ext3/ext4 journal when evidence is mounted read-only: ro,noload, blockdev --setro, and what a skipped replay costs."
sources: ["https://www.kernel.org/doc/html/latest/admin-guide/ext4.html", "https://man7.org/linux/man-pages/man8/mount.8.html", "https://man7.org/linux/man-pages/man8/blockdev.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing journal replay on mounted evidence

**Goal:** a write blocker protects the physical device, but when you mount an image or a software-protected device the filesystem driver may still write. Know the safe options.

## Linux ext3/ext4
```bash
# loop-mount an image read-only and refuse journal replay
mount -o ro,loop,noload,offset=$((2048*512)) image.dd /mnt/ext4
# or make the block device itself read-only first
blockdev --setro /dev/sdb
blockdev --getro /dev/sdb   # prints 1 if read-only
```
- `-o ro` alone is not enough: the mount(8) page says ext3 and ext4 replay the journal if the filesystem is dirty, even when mounted read-only. It recommends mounting with `ro,noload`, or setting the block device itself read-only with blockdev(8). The kernel ext4 document says the same.
- `noload` (same as `norecovery`) means the journal is not loaded on mount. The kernel document warns that if the filesystem was not unmounted cleanly, skipping replay leaves it with inconsistencies, so the mounted view can be inconsistent or lack the latest changes.
- `blockdev --setro` does not affect a device already mounted read-write, so set it before any mount attempt.
- Other filesystems have their own options (see the mount(8) page for the filesystem type); this skill does not cover them.

## Gotchas
- Because the unreplayed journal can hold uncommitted transactions, work from a copy and analyse the journal separately instead of replaying it on the evidence.
- Disable desktop auto-mount on analysis workstations so nothing mounts a device before you set it read-only.

## Verify
Hash the image or device before and after mount/unmount; the hashes match.

## Checked
Confirmed against the kernel ext4 admin guide (`ro` still replays the journal; `ro,noload`; `noload` and `norecovery` skip loading; inconsistency warning), the mount(8) man page (`-r`/`-o ro` note on ext3/ext4 replay, blockdev advice) and the blockdev(8) man page (`--setro`, `--getro`, mounted-read-write caveat). Removed unsupported content: ntfs-3g, XFS and btrfs options, Windows (mountmgr, Arsenal Image Mounter), macOS fstab and `mount_apfs`, `jls`/`debugfs` and the Fast Startup note, and the NIST CFTT source (no claims relied on it).

Method: docs-only read of cited pages, 2026-11-09
