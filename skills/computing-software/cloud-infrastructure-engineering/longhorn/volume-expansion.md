---
id: computing-software.cloud-infrastructure-engineering.longhorn.volume-expansion
name: volume-expansion
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [expansion, resize, pvc, filesystem, online-expansion]
level: practitioner
status: docs-checked
description: "Expand Longhorn volumes through the PVC or UI, the filesystem conditions, reverting to a smaller snapshot, encrypted volumes and RWX share managers."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/expansion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: grow a volume and its filesystem.

Expansion resizes the block device, then the filesystem. Online expansion on V1 needs v1.4.0+; V2 needs v1.10.0+ with the NVMe (`NVMf`) or Block Device frontend (UBLK unsupported).

Method 1, PVC: the PVC must be dynamically provisioned from a StorageClass with `allowVolumeExpansion: true` (V2 also `dataEngine: "v2"`). Edit `spec.resources.requests.storage`; the PV updates automatically.

Method 2, UI: Volumes page, Expand Volume, enter the size.

The filesystem is expanded only when the new size is larger, a Linux filesystem exists, it is ext4 or xfs, the size is within the filesystem maximum (16 TiB for ext4), and the block device frontend is used.

After reverting to a smaller snapshot, the filesystem stays at the snapshot size. Attach the volume to a node and fix it:

```bash
mount /dev/longhorn/<volume name> <dir>
umount /dev/longhorn/<volume name>
mount /dev/longhorn/<volume name> <dir>
resize2fs /dev/longhorn/<volume name>   # ext4
xfs_growfs <dir>                        # xfs
```

Encrypted volumes: Kubernetes v1.29+ resizes natively. On v1.25-v1.28 enable the `CSINodeExpandSecret` feature gate and set `csi.storage.k8s.io/node-expand-secret-name` and `csi.storage.k8s.io/node-expand-secret-namespace`. Otherwise run `cryptsetup resize <volume name>` using `CRYPTO_KEY_VALUE`.

RWX: online NFS expansion is automatic since v1.8.0; after an upgrade delete `share-manager-<volume name>` to recreate it. For offline expansion scale the workload to 0, confirm the volume is `detached`, expand, then scale up.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/expansion/ : version prerequisites, PVC and UI methods, filesystem conditions, revert handling, encrypted and RWX volumes. Nothing else was removed.

Method: documentation only; no commands were run.
