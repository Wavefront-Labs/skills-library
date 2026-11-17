---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-storageclass-parameters-and-scheduler
name: lvm-storageclass-parameters-and-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, storageclass, volgroup, vgpattern, scheduler, spaceweighted, capacityweighted, volumeweighted]
level: practitioner
status: docs-checked
description: "Write a Local PV LVM StorageClass: provisioner local.csi.openebs.io, volgroup or vgpattern, fsType choices, shared, formatOptions, and the three node scheduler policies."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/configuration/lvm-create-storageclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Local PV LVM StorageClass uses `provisioner: local.csi.openebs.io` and, under `parameters`, `storage: "lvm"` plus `volgroup: "lvmvg"` (the volume group you created on each node). The page refers to the Storage Classes reference for all supported parameters.

Standard fields, set at the top level of the class:

- `allowVolumeExpansion`: true or false;
- `mountOptions`: whatever the filesystem supports;
- `volumeBindingMode`: `Immediate` or `WaitForFirstConsumer`;
- `reclaimPolicy`: `Retain` or `Delete`;
- `allowedTopologies`;
- `fsType`: `ext2`, `ext3`, `ext4`, `xfs` or `btrfs`.

LVM-specific parameters: `shared` (yes or no), `vgpattern` (a regular expression matching volume group names, as an alternative to a fixed `volgroup`), `volgroup`, `thinProvision` (yes or no), `formatOptions` (extra `mkfs` options as one space-separated string) and `scheduler`.

**Scheduler policies** (driver v0.9.0 and later) decide which node and volume group receive a new volume:

- `SpaceWeighted` is the default. It picks the node with a volume group that has the most free space, honouring `volgroup` or `vgpattern`.
- `CapacityWeighted` picks the node whose volume group has the least allocated capacity.
- `VolumeWeighted` picks the node whose volume group holds the fewest volumes.

Set `scheduler: "CapacityWeighted"` or `"VolumeWeighted"` under `parameters` to change it.

## Checked

2026-11-04. Confirmed against the Local PV LVM Create StorageClass(s) page: provisioner, `storage` and `volgroup`, the standard and LVM parameter tables, and the three scheduler policies with v0.9.0 support. Rewrote the pointer to the full parameter list.

Method: documentation only; no commands were run.
