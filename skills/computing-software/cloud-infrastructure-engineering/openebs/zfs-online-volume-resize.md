---
id: computing-software.cloud-infrastructure-engineering.openebs.zfs-online-volume-resize
name: zfs-online-volume-resize
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, zfs, resize, quota, refquota, zvol, allowvolumeexpansion, btrfs]
level: practitioner
status: docs-checked
description: "Resize a Local PV ZFS volume by editing the PVC, noting how datasets (quota or refquota) and ZVOLs (resize2fs or xfs_growfs) are handled and that btrfs cannot be resized online."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-zfs/advanced-operations/zfs-resize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resizing is done by raising the size in the PVC. What the driver does depends on the volume type:

- **Dataset** (`fstype: zfs`): the driver updates a quota. With the default `quotatype: quota` it updates the `quota` property; with `refquota` it updates the `refquota` property. For a thick-provisioned dataset the corresponding `reservation` or `refreservation` property is updated as well.
- **ZVOL** with ext2, ext3, ext4 or xfs: the driver expands the volume and then grows the filesystem with `resize2fs` or `xfs_growfs`.
- **btrfs**: not supported, because btrfs does not support online resize here.

The StorageClass must have `allowVolumeExpansion: true`. Expansion is online: no application restart is needed. As with the other engines, filesystem expansion does not happen until a pod references the resized volume, so a PVC with no running pod will not grow its filesystem.

The guide's flow: create the class and a 4Gi PVC, deploy a pod, check size with `df`, then edit the PVC to 5Gi and apply. The PVC YAML then shows a `FileSystemResizePending` condition while the node agent works on the pod's node. Keep checking until the condition clears and the capacity field reads 5Gi, then exec into the pod to confirm the mount point shows the new size.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for zfs-resize) in full. Claims match the page; added the thick-provisioning reservation detail. The phrase "as with the other engines" is based on the LVM resize page, not this one.
