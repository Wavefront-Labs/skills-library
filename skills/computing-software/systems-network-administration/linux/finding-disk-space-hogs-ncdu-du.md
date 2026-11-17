---
id: computing-software.systems-network-administration.linux.finding-disk-space-hogs-ncdu-du
name: finding-disk-space-hogs-ncdu-du
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, disk-usage, ncdu, du-sort, du, df, disk-full, deleted-open-files, lsof, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Find what's filling a filesystem fast: du sorted per level, ncdu interactive scans and exports, staying on one filesystem, and hidden culprits like deleted open files."
sources:
  - https://man7.org/linux/man-pages/man1/du.1.html
  - https://dev.yorhel.nl/ncdu/man
  - https://man7.org/linux/man-pages/man8/lsof.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding disk space hogs: du and ncdu

**Goal:** a filesystem is full — find the biggest directories/files in minutes and free space
without deleting something important.

## 1. du, one level at a time
```bash
du -xh --max-depth=1 /var 2>/dev/null     # -x: skip directories on other file systems
du -xh -d1 /var/log                       # -d is short for --max-depth
du -xah /var/lib/docker 2>/dev/null       # -a: include files, not just directories
du -sh --apparent-size file.img; du -sh file.img   # sparse files: logical vs allocated size
du --inodes -x -d1 /var                   # inode usage instead of block usage
```
- `-h` prints human-readable sizes; `--max-depth=0` is the same as `--summarize`.
- Apparent size is usually smaller than device usage, but can be larger because of holes in
  sparse files, internal fragmentation and indirect blocks.
- `--exclude=PATTERN` takes a shell pattern, not a regular expression.
- Sort the output by size, then drill into the largest entry repeatedly.

## 2. ncdu
```bash
ncdu -x /                              # interactive browser; stay on one file system
ncdu -x -o /tmp/root.ncdu /            # export the scan (JSON) instead of opening the browser
ncdu -f /tmp/root.ncdu                 # browse the export elsewhere
ncdu --exclude-kernfs -x /             # skip pseudo file systems such as /proc and /sys
ncdu -rr -x /                          # read-only: no deletion and no shell spawning
```
- `-r` once is an alias for `--disable-delete`; twice it also adds `--disable-shell`.
- A browsed export has refresh, deletion and shell spawning disabled.
- `-O` exports in a binary format with built-in compression, suited to multi-threaded
  (`-t`) scans of trees that may not fit in memory.
- In the browser, `a` toggles disk usage vs apparent size and `g` toggles the size graph.

## 3. When du and df disagree
- **Deleted but open files**: space is not freed until the process closes them. lsof's
  `+L1` selects open files that have been unlinked: `lsof +L1`. Restart or signal the
  owning process.

## Gotchas
- `du` on huge trees is slow; restrict with `-x` and specific paths.
- Do not `rm` a file a daemon still holds open; the space stays allocated.

## Verify
- [ ] `df` shows usage dropping after cleanup (and `lsof +L1` no longer lists the cleaned files).
- [ ] Root cause fixed (rotation, retention, alerting), not just space freed once.

## Checked
2026-11-01: confirmed against the du man page (man7.org), the ncdu manual (dev.yorhel.nl) and the lsof man page (`+L1`). Removed: df usage, find/numfmt, mount-bind recipe, reserved-block, Btrfs/ZFS/Docker/journal commands, ncdu implementation and RAM remarks, sort-flag explanation, interactive-key list beyond a and g.
Method: documentation only; no commands were run.
