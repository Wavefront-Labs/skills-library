---
id: computing-software.systems-network-administration.zfs.zfs-create-filesystem
name: zfs-create-filesystem
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, create, filesystem, dataset, properties, mountpoint]
level: intro
status: docs-checked
description: "Create a ZFS filesystem with zfs create, set properties at creation with -o, create parents with -p, and validate with -n -v before committing."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-create.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a filesystem

```
zfs create [-Pnpuv] [-o property=value]... filesystem
```

Example:

```
zfs create -o compression=lz4 -o mountpoint=/data tank/projects
```

## Flags

- `-o property=value`: set any editable property at creation, as if `zfs set` ran at the same time. Repeatable, but naming the same property twice is an error.
- `-p`: create missing parent datasets. They mount according to their inherited `mountpoint`, and `-o` values are ignored for them. Giving `-p` twice makes the parents `canmount=off`. If the target already exists the command succeeds, which makes scripts idempotent.
- `-n`: dry run. Combine with `-v` or `-P` to validate property names and values. Real creation can still fail on privileges or capacity.
- `-u`: create without mounting.
- `-v`: verbose output about the new dataset.
- `-P`: parsable, tab-separated output: a `create` line (plus `create_ancestors` with `-p`) and a `property` line for each locally set property.

## Mounting

Without `-u`, the filesystem mounts at its inherited `mountpoint`.

## Checked

2026-11-03. Confirmed against zfs-create(8): synopsis and the `-o`, `-p`, `-n`, `-P`, `-u`, `-v` descriptions. Removed the generic hierarchy-planning paragraph.
Method: documentation only; no commands were run.
