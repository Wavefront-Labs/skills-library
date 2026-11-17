---
id: computing-software.systems-network-administration.incus.storage-drivers-compared
name: storage-drivers-compared
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, drivers, comparison, zfs, btrfs, lvm, ceph, cephfs, linstor, truenas, dir]
level: practitioner
status: docs-checked
description: "Choose an Incus storage driver: the nine drivers, which support optimised creation, snapshots, transfers, nesting and quotas, plus the recommendations and mount-option caveat."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/reference/storage_drivers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage driver comparison

Drivers: Directory, Btrfs, LVM, ZFS, Ceph RBD, CephFS, Ceph Object, LINSTOR, TrueNAS.

- Optimised image storage and copy-on-write: all except Directory.
- Optimised instance creation: Btrfs, LVM, ZFS, Ceph RBD, LINSTOR, TrueNAS.
- Optimised snapshots: those plus CephFS.
- Optimised image/volume transfer: Btrfs, ZFS, Ceph RBD only (native send/receive between same-driver pools); otherwise `rsync` for filesystems or raw block copy for VM and block volumes.
- Block based: LVM, Ceph RBD, LINSTOR, TrueNAS.
- Usable inside a container: Directory, Btrfs, ZFS (needs `zfs.delegate`).
- Restore from older (non-latest) snapshots: Directory, Btrfs, LVM, Ceph RBD, CephFS; not ZFS, LINSTOR, TrueNAS.
- Quotas: all. Offered in `incus admin init`: Directory, Btrfs, LVM, ZFS, Ceph RBD.

Advice: ZFS and Btrfs are the best, ZFS more reliable. Dedicate a disk or partition per pool. Loop-backed pools are not for production; Directory is a last resort.

Caveat: the kernel may silently ignore mount options for an already-mounted block file system. Pools sharing a disk should use identical mount options, or separate disks.

## Checked

2026-11-04: confirmed against the Incus storage drivers reference page (feature comparison table, optimised transfer, recommended setup, mount-option caveat). Nothing removed.

Method: documentation only; no commands were run.
