---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-qos-volumeattributesclass
name: rbd-qos-volumeattributesclass
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [rbd-qos, volumeattributesclass, maxreadiops, cgroup-v2, io-max, noisy-neighbor]
level: advanced
status: docs-checked
description: "Limit IOPS and bandwidth on RBD volumes with a VolumeAttributesClass, krbd cgroup v2 parameters, and patching existing PVCs."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/rbd-qos/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RBD QoS sets IOPS and bandwidth limits on block volumes to stop noisy neighbors. It is configured with a `VolumeAttributesClass`, which allows changing limits on existing volumes without recreation through the ControllerModifyVolume CSI operation. The default krbd mounter enforces limits through the cgroup v2 `io.max` controller.

Requirements: Kubernetes v1.34 or newer (VolumeAttributesClass is GA there), cgroup v2 on nodes, and Linux kernel 5.8 or newer.

Parameters, all optional (examples from the page):
- `maxReadIops`: "1000"
- `maxWriteIops`: "2000"
- `maxReadBps`: "104857600" (100 MiB/s)
- `maxWriteBps`: "209715200" (200 MiB/s)

New deployments: the default `storageclass.yaml` already includes the modify and publish secret references. Create the class with `kubectl create -f deploy/examples/csi/rbd/volumeattributesclass-cgroup.yaml`, then create a PVC with the VolumeAttributesClass. Change an existing volume by patching:
```
kubectl patch pvc rbd-pvc-qos -p '{"spec":{"volumeAttributesClassName":"rook-ceph-rbd-cgroup-qos"}}'
```
One pod can mount several volumes with different limits by using different classes.

Upgraded clusters: StorageClass parameters are immutable, so back up with `kubectl get storageclass rook-ceph-block -o yaml`, delete it, add the modify-secret and publish-secret parameters, recreate it, create the VolumeAttributesClass and patch existing PVCs. Deleting a StorageClass leaves existing PVs and PVCs intact, but new PVCs fail until it returns.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (rbd-qos) against this skill: 19 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
