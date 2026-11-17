---
id: computing-software.systems-network-administration.incus.storage-volume-create-attach
name: storage-volume-create-attach
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage-volume, custom-volume, attach, block, filesystem, iso, content-type]
level: practitioner
status: docs-checked
description: "Create and attach Incus custom storage volumes: filesystem, block and iso content types, attach syntax, and which are restricted to VMs or single attachment."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom volumes: create and attach

Content types:
- `filesystem` (default): can be shared between instances.
- `block` (`--type=block`): VMs only; never attach to more than one VM at once.
- `iso`: made by import, VMs only, read-only so it is safe to share.

```
incus storage volume create <pool> <volume> [options]
incus storage volume create <pool> <volume> --type=block
incus storage volume import <pool> /path/to/file.iso <volume> --type=iso
incus storage volume attach <pool> <fs_volume> <instance> <device> <location>
incus storage volume attach <pool> <block_volume> <instance> <device>
incus config device add <instance> <device> disk pool=<pool> source=<volume> [path=<location>]
```

- Block and iso volumes cannot attach to containers; filesystem volumes cannot attach to running VMs using 9p.
- `--target=<member>` places a volume on a cluster member. Volumes are reachable from any member only on Ceph (`ceph`, `cephfs`), `lvmcluster`, `linstor` and `truenas` pools.

## Checked

2026-11-04: confirmed against the Incus storage volumes how-to (content types, create/import/attach syntax, attach restrictions, `--target`, volumes visible from any member only on listed drivers). Nothing removed.

Method: documentation only; no commands were run.
