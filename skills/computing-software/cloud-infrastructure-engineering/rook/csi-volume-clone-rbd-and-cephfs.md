---
id: computing-software.cloud-infrastructure-engineering.rook.csi-volume-clone-rbd-and-cephfs
name: csi-volume-clone-rbd-and-cephfs
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [volume-clone, datasource, persistentvolumeclaim, pvc-clone, rbd, cephfs]
level: practitioner
status: docs-checked
description: "Clone an RBD or CephFS PVC by naming the source PVC in dataSource, with the encryption and storage class constraints for each driver."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Ceph-CSI/ceph-csi-volume-clone/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CSI volume cloning lets you specify an existing PVC in `dataSource`. The back end then creates an exact duplicate of that volume at provisioning, rather than a new empty one. The clone can be consumed like any standard volume.

RBD clone: in `pvc-clone`, `dataSource` is the name of a PVC already created by the RBD CSI driver and its kind is `PersistentVolumeClaim`. The `storageClassName` can be any RBD storage class, not necessarily the parent's. Constraints:
- The provisioner must be the same for parent and clone.
- Encrypted to encrypted and non-encrypted to non-encrypted work.
- Encrypted to non-encrypted, or non-encrypted to encrypted, does not.

Verify with `kubectl get pvc`: both `rbd-pvc` and `rbd-pvc-clone` show Bound, with the same size (1Gi in the example) and RWO.

CephFS clone: requires Kubernetes v1.16 or newer and Ceph-CSI driver v3.1.0 or newer. In `pvc-clone`, `dataSource` is a PVC created by the CephFS CSI driver (kind `PersistentVolumeClaim`), and the clone's `storageClassName` must be the same as the source PVC's. The example shows `cephfs-pvc` and `cephfs-pvc-clone` Bound as RWX on `rook-cephfs`.

Each page ends with a cleanup step that deletes the example resources.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-csi-volume-clone) against this skill: 12 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
