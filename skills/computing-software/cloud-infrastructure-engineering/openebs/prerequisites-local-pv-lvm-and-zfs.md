---
id: computing-software.cloud-infrastructure-engineering.openebs.prerequisites-local-pv-lvm-and-zfs
name: prerequisites-local-pv-lvm-and-zfs
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [prerequisites, local-pv, lvm, zfs, volume-group, zpool, loopback, topology]
level: practitioner
status: docs-checked
description: "Prepare nodes for Local PV LVM (lvm2, dm-snapshot, a volume group) and Local PV ZFS (zfsutils-linux and a zpool), including the loopback-file option for testing only."
sources:
  - https://openebs.io/docs/quickstart-guide/prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both volume-manager engines need a pre-built pool on every node that will host volumes.

**Local PV LVM.** Every node needs the `lvm2` utilities and the `dm-snapshot` kernel module loaded. Find the disk to use, then create a physical volume and a volume group on all nodes, because the LVM driver provisions out of that group. The page's example volume group is named `lvmvg`, built with `pvcreate` on a device followed by `vgcreate lvmvg` on it. For testing only, a loopback device can stand in: the page creates a sparse file with `truncate`, attaches it with `losetup -f --show`, and builds the group on the resulting loop device.

**Local PV ZFS.** Every node needs `zfsutils-linux` (the page uses `apt-get install zfsutils-linux`) and a ZFS pool. The pool can be striped, mirrored or raidz; with a spare disk such as `/dev/sdb`, the page creates a striped pool named `zfspv-pool` with `zpool create`. A loopback-backed pool exists for testing only. Verify with `zpool status` and expect the pool ONLINE with no known data errors.

If you want to place ZFS volumes in a particular zone or building, label the nodes and configure custom topology keys, then reference that key in the StorageClass. The prerequisites page points to the FAQ for the exact procedure.

The page's supported-versions list names LVM 2 and ZFS 0.8.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for quickstart-guide/prerequisites) in full. Claims match the page; added the supported versions.
