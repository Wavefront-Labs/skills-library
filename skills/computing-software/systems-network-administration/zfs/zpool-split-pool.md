---
id: computing-software.systems-network-administration.zfs.zpool-split-pool
name: zpool-split-pool
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, split, mirror, clone-pool, altroot]
level: advanced
status: docs-checked
description: "Split a mirrored ZFS pool into two with zpool split: which devices move, -n dry run, -R altroot, -l keys, -o properties and requirements."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-split.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool split

```
zpool split [-gLlnP] [-o property=value]... [-R root] pool newpool [device]...
```

Detaches devices from a mirrored pool to create a new pool that is a replica of the original at the moment of the split. `newpool` gets a new GUID.

## Requirements

- Every vdev in the pool must be a mirror.
- The pool cannot be resilvering.
- A checkpoint blocks it (see zpool-checkpoint).

## Which devices move

By default the last device in each mirror goes to `newpool`. Devices you name go instead, and mirrors you do not name still give up their last device.

```
zpool split -n tank backup
zpool split tank backup
zpool split -R /mnt/backup tank backup sdb
```

## Options

- `-n`: dry run; prints the expected `newpool` configuration without splitting.
- `-R root`: set `altroot` on `newpool` and import it automatically.
- `-o property=value`: set a pool property on `newpool`; repeatable.
- `-l`: request encryption keys as `newpool` comes online. With `keylocation=prompt` it blocks for the key; without `-l`, encrypted datasets stay unavailable until keys are loaded.
- `-g`: show GUIDs instead of names (usable with detach, offline, remove, replace).
- `-L`: resolve symlinks to real block device paths. `-P`: full paths.

## Checked

2026-11-03. Pages read: zpool-split(8), zpool-checkpoint(8).

Confirmed: requirements (all mirrors, not resilvering), default last-device selection, new GUID, -n, -R, -o, -l, -g, -L, -P and the checkpoint prohibition.

Removed or corrected: the claim that without -R the new pool stays exported, which the page does not state.

Method: documentation only; no commands were run.
