---
id: computing-software.systems-network-administration.zfs.zpool-remove-vdev
name: zpool-remove-vdev
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, remove, device-removal, evacuate, mapping-table]
level: advanced
status: docs-checked
description: "Remove spares, cache, log and top-level vdevs from a ZFS pool with zpool remove: restrictions, -n and -p estimates, -w and -s cancellation."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-remove.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool remove

```
zpool remove [-npw] pool device...
zpool remove -s pool
```

Removes hot spares, cache devices, log devices, and mirrored or non-redundant primary top-level vdevs, including dedup and special vdevs. Name a mirrored top-level vdev by its name, e.g. `mirror-2`. To remove a redundant member of a mirror, use `zpool detach` instead.

```
zpool remove -n tank mirror-1
zpool remove tank mirror-1
zpool remove -s tank
```

## Top-level vdev removal

Restrictions:

- The primary pool storage cannot contain a top-level raidz or dRAID vdev.
- All top-level vdevs must have the same ashift.
- Keys for all encrypted datasets must be loaded.
- The `device_removal` feature must be enabled.
- No checkpoint may exist (see zpool-checkpoint).

Behaviour:

- Total pool capacity shrinks.
- Allocated data is copied to the remaining devices; the command returns immediately and evacuation continues in the background.
- An I/O error during removal cancels the removal.

## Options

- `-n`: dry run; prints the estimated memory the mapping table will use after removal (nonzero only for top-level vdevs).
- `-p`: with `-n`, exact parsable values.
- `-w`: block until removal completes.
- `-s`: stop and cancel an in-progress top-level removal.

Track progress in `zpool status`, or script with `zpool wait -t remove tank`.

## Checked

2026-11-03. Pages read: zpool-remove(8), zpool-checkpoint(8), zpool-wait(8).

Confirmed: supported device types, the four restrictions, device_removal feature, background evacuation, I/O error cancellation, -n/-p/-w/-s, and the checkpoint prohibition.

Method: documentation only; no commands were run.
