---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-fsgroup-volume-permissions
name: lvm-fsgroup-volume-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, fsgroup, fsgrouppolicy, csi-driver, podfsgroupchangepolicy, permissions, non-root]
level: advanced
status: docs-checked
description: "Control volume ownership for non-root pods on Local PV LVM using the CSIDriver FSGroupPolicy values and the Pod fsGroupChangePolicy OnRootMismatch or Always."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-fs-group
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
fsGroup lets a non-root process access a volume. Kubelet owns ownership and permission changes: after the CSI driver's `NodePublishVolume` mounts the volume, kubelet applies the ownership and permissions if required. Two settings decide when.

**Storage admin: `FSGroupPolicy` in the CSIDriver spec.**

- `ReadWriteOnceWithFSType`: change ownership and permissions to the pod's `fsGroup` when the access mode is RWO and `fsType` is set.
- `None`: mount without trying to change ownership or permissions.
- `File`: always try to apply `fsGroup`, whatever the `fsType` or access mode.

**Application developer: `fsGroupChangePolicy` in the pod security context** (the doc names it `PodFSGroupChangePolicy`).

- `OnRootMismatch`: only change permissions and ownership if the top-level directory does not already match the expected ones.
- `Always`: always change them to match `fsGroup`.

The page's test plan combines the three CSIDriver policies with the PVC access mode. The LVM CSI driver supports only ReadWriteOnce, and for ReadWriteOnce `File` and `ReadWriteOnceWithFSType` are equal. Expected results:

1. `ReadWriteOnceWithFSType` or `File`: a non-root process can access the volume.
2. `None`: a non-root process cannot access the volume.
3. Any policy: a root process can access the volume.
4. If `fsGroup` is missing from the Pod spec, a non-root process cannot access the volume.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-fs-group) in full. Policy values, their meanings and the test plan are as the page states. Replaced the earlier unsourced "choose cluster policy first" advice with the page's expected results.
