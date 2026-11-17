---
id: computing-software.cloud-infrastructure-engineering.rook.cephfilesystem-subvolumegroup-crd
name: cephfilesystem-subvolumegroup-crd
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephfilesystemsubvolumegroup, subvolumegroup, pinning, distributed, datapoolname, quota]
level: advanced
status: docs-checked
description: "Create CephFS subvolume groups with a CephFilesystemSubVolumeGroup CR, including quota, data pool layout and the single-choice pinning options."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Shared-Filesystem/ceph-fs-subvolumegroup-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A CephFS subvolume group is a directory level above subvolumes, used to apply policies such as file layouts across a set of subvolumes. Rook creates them with the `CephFilesystemSubVolumeGroup` CRD, for example on the CephFilesystem `myfs` in namespace `rook-ceph`.

Fields:
- `name`: the subvolume group name; if not set, the metadata name is used.
- `filesystemName`: the metadata name of the CephFilesystem CR that will hold the group.
- `quota`: quota size of the group.
- `dataPoolName`: use this data pool for the group's layout instead of the default data pool.
- `clusterID`: can be set explicitly in the spec; otherwise Rook generates it.
- `pinning`: spreads load across MDS ranks predictably.
  - `distributed`: 0 or 1; set 0 to disable.
  - `export`: 0 to 256; set -1 to disable.
  - `random`: 0.0 to 1.0; set 0.0 to disable.

Only one of `export`, `distributed` and `random` can be set at a time. By default pinning is `distributed=1`.

Workflow: create the CephFilesystem CR, then the CephFilesystemSubVolumeGroup CR, then create a StorageClass for the subvolume group so volumes are provisioned within it. Unspecified settings take suitable defaults.

## Checked

2026-11-03. Confirmed against the CephFilesystemSubVolumeGroup CRD page: the name, filesystemName, quota, dataPoolName and clusterID fields, pinning ranges for distributed, export and random, the one-pinning-choice rule and the distributed=1 default. Removed: nothing.

Method: documentation only; no commands were run.
