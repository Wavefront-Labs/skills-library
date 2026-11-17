---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-online-volume-resize
name: lvm-online-volume-resize
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, resize, allowvolumeexpansion, lvextend, online-expansion, filesystemresizepending]
level: practitioner
status: docs-checked
description: "Expand a Local PV LVM volume online by editing the PVC, with allowVolumeExpansion true, FileSystemResizePending, and the Kubernetes 1.23 need for block and btrfs."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-resize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To resize a Local PV LVM volume, change the requested size in the PVC and apply it. The driver expands the volume with `lvextend` using the `-r` option, which also resizes the filesystem.

Requirements:

- the StorageClass that provisioned the PVC must set `allowVolumeExpansion: true`;
- online expansion for `Block` mode and for the `btrfs` filesystem needs **Kubernetes 1.23 or later**.

Expansion is **online**: the volume can be in use and the application does not have to restart. One caveat: filesystem expansion does not happen until an application pod references the resized volume, so with no running pod the filesystem is not grown.

The guide's worked example uses a class named `openebs-lvmpv` with `fstype: "ext4"` and a volume group, a 4Gi PVC and a pod mounting it. Raising the PVC to 5Gi first leaves the claim showing the old capacity with a `FileSystemResizePending` condition ("waiting for user to (re-)start a pod to finish file system resize of volume on node"). The resize request goes to the node running the pod, the LVM driver node agent resizes the filesystem, and the condition disappears once the PVC status capacity reads the new size. Re-check the PVC YAML until `FileSystemResizePending` is gone, then confirm inside the pod with `df -h` on the mount.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-resize) in full. All claims match the page; no claims were changed.
