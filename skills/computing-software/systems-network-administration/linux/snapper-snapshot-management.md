---
id: computing-software.systems-network-administration.linux.snapper-snapshot-management
name: snapper-snapshot-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, snapper, btrfs-snapshot, snapper-rollback, timeline-snapshots, snap-pac, opensuse]
level: practitioner
status: docs-checked
description: "Manage Btrfs (or thin LVM) snapshots with snapper: configs, timeline and cleanup algorithms, pre/post pairs around package changes, diff/undochange and rollback."
sources:
  - https://github.com/openSUSE/snapper/blob/master/doc/snapper.xml.in
  - https://github.com/openSUSE/snapper/blob/master/doc/snapper-configs.xml.in
  - https://github.com/openSUSE/snapper/blob/master/data/default-config
  - https://github.com/openSUSE/snapper/blob/master/data/Makefile.am
  - https://github.com/openSUSE/snapper/blob/master/doc/snapper-zypp-plugin.xml.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# snapper

## Configs
```bash
snapper -c root create-config /            # creates /.snapshots subvolume and /etc/snapper/configs/root
snapper -c home create-config /home
snapper list-configs
```
`/etc/snapper/configs/root` key settings:
```
TIMELINE_CREATE="yes"
TIMELINE_LIMIT_HOURLY="5"
TIMELINE_LIMIT_DAILY="7"
TIMELINE_LIMIT_WEEKLY="0"
TIMELINE_LIMIT_MONTHLY="0"
NUMBER_LIMIT="20"                # snapshots kept by number cleanup (upstream default 50)
SPACE_LIMIT="0.5"                # max fraction of the filesystem snapshots may use (btrfs only)
```
Timers: `snapper-timeline.timer`, `snapper-cleanup.timer`.

## Pre/post around changes
On openSUSE, snapper-zypp-plugin creates pre/post snapshots around zypper transactions; other package managers need their own integration.
Manual: `snapper -c root create --type pre --print-number -d "nginx upgrade"` → change → `snapper create --type post --pre-number N`.

## Inspect and undo
```bash
snapper -c root list
snapper -c root status 41..42              # files changed
snapper -c root diff 41..42 /etc/nginx/nginx.conf
snapper -c root undochange 41..42 /etc/nginx/nginx.conf   # revert specific files
snapper rollback 41                         # btrfs only: snapshots the current system read-only, makes a read-write snapshot of 41 and sets it to boot; reboot
```
Rollback is only supported on btrfs and requires a properly configured system (the system boots from the btrfs default subvolume); otherwise prefer file-level `undochange`.

## Gotchas
- Snapshots of `/` that include `/var/lib/mysql`, `/var/log` waste space and roll back data — put them in separate subvolumes.
- Space accounting: deleted files stay referenced by snapshots; `btrfs filesystem usage /` not `df`.
- Many snapshots slow full qgroup accounting (see the btrfs quota documentation).

## Verify
- [ ] `snapper list` shows timeline and pre/post entries; cleanup keeps counts at the limits.

## Checked
Checked 2026-10-26 against the openSUSE/snapper repository (pushed 2026-10-22): doc/snapper.xml.in, doc/snapper-configs.xml.in, data/default-config and data/Makefile.am.
Confirmed: `create-config`, `list-configs`, `create --type pre|post --pre-number -p -d`, `status`, `diff`, `undochange` with `N..M` ranges, `rollback` behaviour, config keys TIMELINE_CREATE, TIMELINE_LIMIT_*, NUMBER_LIMIT, SPACE_LIMIT (default 0.5, btrfs only), the snapper-timeline and snapper-cleanup timers, and the zypp plugin.
Wrong in the draft: rollback does not simply make 41 the default subvolume (it takes a read-only snapshot of the current system and a read-write snapshot of 41); NUMBER_LIMIT is a count of snapshots kept by number cleanup, not of pre/post pairs.
Removed as unconfirmed: snap-pac, the dnf plugin package and grub-btrfs advice.
Method: documentation only; no commands were run.
