---
id: computing-software.systems-network-administration.zfs.zpool-add-vdevs
name: zpool-add-vdevs
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, add, vdev, cache, l2arc, ashift]
level: practitioner
status: docs-checked
description: "Add vdevs to an existing ZFS pool with zpool add, dry-run with -n, add cache devices, and understand the ashift and replication mismatch overrides."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-add.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding vdevs

```
zpool add [-fgLnP] [--allow-in-use --allow-replication-mismatch --allow-ashift-mismatch] [-o property=value] pool vdev...
```

Examples:

```
zpool add -n tank mirror sda sdb
zpool add tank mirror sda sdb
zpool add tank cache sdc sdd
```

The new space is available to datasets immediately. Adding a mirror to a pool of two-way mirrors keeps the layout consistent.

## Flags

- `-n`: dry run; shows the resulting configuration. The add can still fail afterwards.
- `-f`: force vdevs that appear in use, have conflicting ashift, or conflict in replication level.
- `-g`: show vdev GUIDs instead of names (usable in `detach`, `offline`, `remove`, `replace`).
- `-L`: show real paths (resolving symlinks); `-P`: full paths.
- `-o ashift=...`: the only supported property.
- `--allow-ashift-mismatch`: permit different sector sizes. Side effect: future device removal operations will be prohibited.
- `--allow-in-use`, `--allow-replication-mismatch`: override those checks.

## Cache devices

Cache (L2ARC) devices fill gradually from memory, possibly taking over an hour. Watch with:

```
zpool iostat -v tank 5
```

Run `-n` first to see the resulting configuration. Top-level raidz or draid vdevs cannot be removed later (see zpool-remove-vdev), and adding top-level vdevs with different sector sizes prohibits future device removal.

## Checked

2026-11-03. Pages read: zpool-add(8), zpool-remove(8).

Confirmed: synopsis, -f, -g, -L, -n, -P, -o ashift as the only property, the --allow-* flags, the ashift-mismatch removal side effect, and the cache-device example with the over-an-hour fill time.

Removed or corrected: the unsupported sentence about wrong redundancy.

Method: documentation only; no commands were run.
