---
id: computing-software.systems-network-administration.linux.mdadm-write-intent-bitmap
name: mdadm-write-intent-bitmap
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mdadm, write-intent-bitmap, mdadm-bitmap, raid-resync, internal-bitmap, software-raid]
level: advanced
status: docs-checked
description: "Use md write-intent bitmaps to make post-crash resyncs and re-added disks take minutes instead of hours: add/remove bitmaps, chunk size and cost."
sources:
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/md.4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# md write-intent bitmaps

**What:** a bitmap of regions with in-flight writes. After an unclean shutdown, or when a briefly
disconnected member is `--re-add`ed, md resyncs only dirty regions instead of the whole array.

## Check / add / remove
```bash
cat /proc/mdstat                       # shows a bitmap line when one is configured
mdadm --detail /dev/md0                    # reports the intent bitmap
mdadm --grow /dev/md0 --bitmap=internal --bitmap-chunk=128M
mdadm --grow /dev/md0 --bitmap=none            # remove the bitmap
mdadm --examine-bitmap /dev/sda1               # on-disk bitmap of a member
```
An internal bitmap's chunk size defaults to 64 MiB, or larger if needed to fit the bitmap in the available space.

## Re-add instead of full rebuild
```bash
mdadm /dev/md0 --re-add /dev/sdb1     # recovers only the blocks flagged in the bitmap, based on the member's event count
```
With persistent metadata (superblocks) and a bitmap, re-adding a removed device is done automatically.

## Performance
`--bitmap-chunk` sets how much storage each bit covers; a write-intent bitmap is also required for write-behind (`--write-behind`).

## Gotchas
- A bitmap lets a removed device be re-added cheaply; a brand-new replacement disk has no matching data, so it is rebuilt in full.

## Verify
- [ ] `/proc/mdstat` shows a bitmap line; after a test unclean reboot, resync completes far faster than a full one.

## Checked

Checked against the mdadm main branch (mdadm.8.in `--bitmap`, `--bitmap-chunk`, `--re-add`, `--examine-bitmap`, md.4 bitmap write-intent logging), repository last pushed 2026-10-08.
Confirmed: `--bitmap=internal|clustered|lockless|none`; internal bitmap chunk defaults to 64 MiB; `--examine-bitmap` (-X); `--re-add` recovers only flagged blocks; bitmap needed for write-behind; the two optimisations (resync after unclean shutdown, re-add).
Removed unconfirmed claims: the >100 GB default, the example output strings, per-write latency remarks, and the rule that grows need the bitmap removed first.

Method: documentation only; no commands were run.
