---
id: computing-software.systems-network-administration.incus.storage-zfs-driver
name: storage-zfs-driver
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, zfs, refquota, zfs-clone-copy, zfs-delegate, snapshots, zpool]
level: advanced
status: docs-checked
description: "Run Incus on ZFS: requirements, how datasets and clones are used, restore limits, quota vs refquota, and the zfs.* keys (clone_copy, remove_snapshots, use_refquota, delegate)."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/reference/storage_zfs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS driver

- Install `zfsutils-linux`; ZFS wants plenty of RAM. Dataset delegation and idmap need ZFS 2.2+.
- Images and custom volumes are filesystems or volumes; instances and snapshots use ZFS snapshots and clones.
- Compression is on by default for pools Incus creates; trim is automatic on new pools with ZFS 0.8+.
- Incus assumes control of the pool or dataset: do not create child datasets there. Removed-but-referenced objects are renamed under `deleted/`.

Limitations:
- Only the latest snapshot can be restored; older ones can seed new instances. `zfs.remove_snapshots` discards newer snapshots on restore.
- With `zfs.clone_copy=true`, copies use snapshots, making older restores harder.
- I/O limits have little effect.

Quotas: `quota` (includes snapshots and clones) is the default; `zfs.use_refquota` switches to `refquota`; `zfs.use_reserve_space` adds a reservation.

Keys: `zfs.clone_copy` (pool), `volume.zfs.remove_snapshots` (pool), `zfs.remove_snapshots`, `zfs.use_refquota`, `zfs.use_reserve_space` (volume), `zfs.delegate` (container volume, lets the container run `zfs`).

## Checked

2026-11-04: confirmed against the Incus ZFS storage driver reference page (package, ZFS 2.2 requirement, compression and trim, `deleted/` renaming, restore limitation, quota options, `zfs.delegate`). Nothing removed.

Method: documentation only; no commands were run.
