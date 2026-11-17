---
id: computing-software.systems-network-administration.zfs.zfs-rename-datasets
name: zfs-rename-datasets
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, rename, dataset, snapshot, rolling-snapshots, mountpoint]
level: practitioner
status: docs-checked
description: "Rename ZFS filesystems, volumes and snapshots with zfs rename, including -p, -u, -f and recursive snapshot renames for rolling schemes."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-rename.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renaming

Forms:

```
zfs rename [-f] filesystem|volume|snapshot filesystem|volume|snapshot
zfs rename -p [-f] filesystem|volume filesystem|volume
zfs rename -u [-f] filesystem filesystem
zfs rename -r snapshot snapshot
```

## Options

- `-f`: force-unmount filesystems that must be unmounted for the rename. No effect with `-u`.
- `-p`: create missing parent datasets (mounted per inherited `mountpoint`). Repeating `-p` creates them with `canmount=off`.
- `-u`: skip remounting. Datasets with `mountpoint` set to `legacy` or `none` are never unmounted either way.
- `-r`: recursively rename snapshots of descendants. Only snapshots can be renamed recursively.

## Notes

- A filesystem or volume can move anywhere in the hierarchy; a snapshot can only be renamed within its parent dataset.
- A renamed filesystem may get a new mountpoint, so it is unmounted and remounted there.

## Rolling snapshots

Destroy the oldest, shift the rest with `rename -r`, then create the newest:

```
zfs destroy -r pool/users@7daysago
zfs rename -r pool/users@6daysago @7daysago
zfs rename -r pool/users@yesterday @2daysago
zfs snapshot -r pool/users@yesterday
```

## Checked

2026-11-03. Confirmed against zfs-rename(8): all four synopsis forms, `-f`, `-p`, `-u`, `-r`, snapshot-within-parent rule, remount on new mountpoint, and the rolling-snapshot example. Removed the unsupported `-u` advice.
Method: documentation only; no commands were run.
