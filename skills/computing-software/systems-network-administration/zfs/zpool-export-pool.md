---
id: computing-software.systems-network-administration.zfs.zpool-export-pool
name: zpool-export-pool
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, export, migrate, unmount, portable]
level: intro
status: docs-checked
description: "Export a ZFS pool with zpool export before moving disks: unmount behaviour, -a, -f and its corruption risk, shared spares and whole-disk labels."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-export.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool export

```
zpool export [-f] -a | pool...
```

Exporting prepares a pool to move to another system.

```
zpool export tank
zpool export -a
```

## Behaviour

- All datasets in the pool are unmounted first.
- Exported devices are marked as exported, but they remain in use by other subsystems. Once moved to another system they can be imported if enough devices are present.
- Without `-f`, a pool cannot be exported while a shared spare it uses is actively in use.

## Options

- `-a`: export all pools currently imported.
- `-f`: forcibly unmount all datasets and allow export of a pool with an active shared spare. The man page warns this may lead to potential data corruption.

## Moving between platforms

Use whole disks rather than partitions: ZFS can then write portable EFI labels, which allows disks to move between platforms of different endianness.

## On the new system

```
zpool import            # list importable pools
zpool import tank
```

If a device was removed without exporting, import needs `-f` because ZFS cannot tell whether the export failed or another host is using the pool. See zpool-import-pools.

## Checked

2026-11-03. Pages read: zpool-export(8), zpool-import(8).

Confirmed: synopsis, unmounting, -a, -f and its corruption warning, shared-spare rule, whole disks and EFI labels for endianness portability, and import needing -f after a device was removed without export.

Method: documentation only; no commands were run.
