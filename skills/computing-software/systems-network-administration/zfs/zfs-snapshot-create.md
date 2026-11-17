---
id: computing-software.systems-network-administration.zfs.zfs-snapshot-create
name: zfs-snapshot-create
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, snapshot, recursive-snapshot, snapdir, atomic]
level: intro
status: docs-checked
description: "Create atomic ZFS snapshots with zfs snapshot, take recursive snapshots with -r, and browse them under .zfs/snapshot."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating snapshots

```
zfs snapshot [-r] [-o property=value]... dataset@snapname...
```

`zfs snap` is an alias. Example:

```
zfs snapshot -r tank/home@2026-11-03
zfs snapshot tank/db@pre-upgrade tank/web@pre-upgrade
```

## Semantics

- A snapshot is an atomic, consistent image of the dataset at one point in time, including every change from system calls completed before then.
- With `-r`, snapshots of all descendant datasets are created at the same time, so the set is consistent across the tree.
- Several `dataset@snapname` arguments can be passed in one command.
- `-o property=value` sets a property on the snapshot (user properties work).

## Access

Snapshots mount on demand under the `.zfs/snapshot` directory at the dataset root.

## Housekeeping

- Remove: `zfs destroy -r pool/home@snapname`
- Rename a set: `zfs rename -r old@name new@name`, handy for rolling-snapshot schemes
- Related: `zfs clone`, `zfs rollback`, `zfs send`, `zfs hold`, `zfs bookmark`

## Checked

2026-11-03. Confirmed against zfs-snapshot(8) (synopsis, `snap` alias, atomic and simultaneous recursive snapshots, `-o`, `.zfs/snapshot` on-demand mount, destroy and rename examples). Removed the unsupported naming advice and the claim about users not needing admin help.
Method: documentation only; no commands were run.
