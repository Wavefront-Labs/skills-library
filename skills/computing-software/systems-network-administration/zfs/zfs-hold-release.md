---
id: computing-software.systems-network-administration.zfs.zfs-hold-release
name: zfs-hold-release
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, hold, release, holds, snapshot-protection, ebusy]
level: practitioner
status: docs-checked
description: "Protect ZFS snapshots from deletion with zfs hold, list holds with zfs holds, and remove them with zfs release."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-hold.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Holds

A hold is a named reference on a snapshot. While any hold exists, `zfs destroy` on that snapshot fails with EBUSY.

## Add

```
zfs hold [-r] tag snapshot...
```

`tag` is your name for the hold, unique only within that snapshot. `-r` applies the hold to the snapshots of all descendant filesystems.

```
zfs hold -r replication-base tank/data@2026-11-03
```

## List

```
zfs holds [-rHp] snapshot...
```

- `-r`: include descendant snapshots
- `-H`: no headers, tab-delimited
- `-p`: timestamps as Unix epoch values

## Release

```
zfs release [-r] tag snapshot...
```

The tag must exist on every target snapshot. `-r` releases recursively.

## Related

- Send holds along with a stream using `zfs send -h`.

Destroying a held snapshot with `zfs destroy -d` marks it for deferred destruction; it disappears when the last hold is released. Check `userrefs` to see how many holds remain.

## Checked

2026-11-03. Confirmed against zfs-hold(8) (hold, holds, release synopsis and flags, tag namespace, EBUSY), zfs-destroy(8) (`-d`, `userrefs`) and zfs-send(8) (`-h`). Removed the generic use-case bullets.
Method: documentation only; no commands were run.
