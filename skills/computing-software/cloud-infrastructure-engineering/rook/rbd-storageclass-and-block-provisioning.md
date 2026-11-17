---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-storageclass-and-block-provisioning
name: rbd-storageclass-and-block-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [storageclass, rbd, rook-ceph-block, imagefeatures, reclaimpolicy, csi-secrets]
level: intro
status: docs-checked
description: "Create a CephBlockPool and RBD StorageClass with the CSI secret parameters, then consume it with PVCs; reclaimPolicy Retain needs manual rbd rm."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/block-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before Rook can provision block volumes, create a CephBlockPool (replicated size 3 with `failureDomain: host` needs OSDs on three different nodes) and a StorageClass. Create the class with `kubectl create -f deploy/examples/csi/rbd/storageclass.yaml`.

Key StorageClass parameters in the example:
- `imageFormat: "2"` and `imageFeatures: layering`
- secrets: `csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner` (also controller-expand, controller-publish and controller-modify) and `node-stage-secret-name: rook-csi-rbd-node` (also node-publish), each with a matching `-namespace` set to `rook-ceph`
- `csi.storage.k8s.io/fstype: ext4`
- `reclaimPolicy: Delete` and `allowVolumeExpansion: true`

If the operator runs in another namespace, change the provisioner prefix to match, for example `my-namespace.rbd.csi.ceph.com`.

With `reclaimPolicy: Retain`, an RBD image stays after its PV is deleted and must be removed manually with `rbd rm`.

Consume it with the sample apps: `kubectl create -f mysql.yaml` and `wordpress.yaml`, then `kubectl get pvc` shows two RWO claims (20Gi in the example) bound.

Teardown: delete wordpress and mysql, then the CephBlockPool `replicapool` and the `rook-ceph-block` StorageClass.

QoS limits can be applied dynamically via a VolumeAttributesClass, and a block image can also be mounted directly with the toolbox.

## Checked

2026-11-03. Confirmed against the Block Storage page: the StorageClass parameters, secret names, Retain needing manual rbd rm, the sample apps and teardown, and the QoS VolumeAttributesClass mention. Removed: nothing.

Method: documentation only; no commands were run.
