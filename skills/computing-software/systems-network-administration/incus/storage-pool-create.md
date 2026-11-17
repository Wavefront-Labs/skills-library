---
id: computing-software.systems-network-administration.incus.storage-pool-create
name: storage-pool-create
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, storage-pool, create, loop-backed, zfs, dir, source]
level: practitioner
status: docs-checked
description: "Create Incus storage pools with incus storage create: driver and source examples, loop-backed default sizing, and creating pools across a cluster with --target."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_pools.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create storage pools

```
incus storage create <pool_name> <driver> [options...]
incus storage create pool2 dir source=/data/incus
incus storage create pool3 zfs source=my-tank
incus storage create pool5 zfs source=my-tank/zvol volume.zfs.block_mode=yes
incus storage create pool6 zfs source=/dev/sdX
```

- With no `source`, Incus makes a loop-backed pool sized at 20% of free disk space, minimum 5 GiB, maximum 30 GiB.
- Incus creates a default pool at init, usually named `default` or `local`.

Cluster: first run on each member with the same name, `incus storage create my-pool zfs source=/dev/sdX size=10GiB --target=vm01` (state: pending). Then finalise with `incus storage create my-pool zfs` (no `--target`).

Most drivers are local per member; volumes on one member are invisible to others. `ceph`, `cephfs` and `cephobject` pools are shared by all members.

## Checked

2026-11-04: confirmed against the Incus storage pools how-to (create syntax and examples, loop-backed default size, default pool name, cluster pending-then-finalise flow, Ceph-based pools shared). Nothing removed.

Method: documentation only; no commands were run.
