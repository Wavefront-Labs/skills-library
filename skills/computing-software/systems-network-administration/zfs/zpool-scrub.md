---
id: computing-software.systems-network-administration.zfs.zpool-scrub
name: zpool-scrub
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, scrub, pause, stop, systemd-timer, data-integrity]
level: intro
status: docs-checked
description: "Run, pause, resume and stop ZFS scrubs with zpool scrub, wait for completion, and schedule periodic scrubs with systemd timers."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scrubbing

A scrub reads all data in the pool and verifies checksums, repairing from redundancy where possible.

```
zpool scrub tank
zpool scrub -w tank        # block until it finishes
zpool scrub -p tank        # pause
zpool scrub tank           # resume
zpool scrub -s tank        # stop
zpool status tank
```

## Rules

- Only one scrub or resilver runs per pool at a time; a scrub cannot start during a resilver.
- A paused scrub stays paused across reboots and export/import until resumed, and resumes from the last on-disk checkpoint in the mode it started.
- `-a` (or `--all`) applies start, `-p` or `-s` to all pools; scrubbing many pools at once adds heavy I/O and memory load.
- Progress can exceed 100% on a live system, and no completion estimate is shown while it does.

## Periodic scrubs on systemd

```
systemctl enable --now zfs-scrub-weekly@tank.timer
systemctl enable --now zfs-scrub-monthly@tank.timer
```

## After a scrub

Check `zpool status -v tank` for files with data errors.

See zpool-scrub-error-and-dates for error scrubs, thorough mode and date ranges.

## Checked

2026-11-03. Pages read: zpool-scrub(8).

Confirmed: start, wait (-w), pause (-p), resume, stop (-s), -a, one scrub or resilver at a time, pause persisting across restart and export/import, progress above 100%, and the systemd weekly and monthly timer units.

Removed or corrected: the advice to restore from a snapshot replica, which the page does not give.

Method: documentation only; no commands were run.
