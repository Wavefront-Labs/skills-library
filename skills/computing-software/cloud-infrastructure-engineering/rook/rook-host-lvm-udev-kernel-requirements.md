---
id: computing-software.cloud-infrastructure-engineering.rook.rook-host-lvm-udev-kernel-requirements
name: rook-host-lvm-udev-kernel-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [prerequisites, lvm2, udev, rbd-module, cephfs-kernel, imagefeatures]
level: practitioner
status: docs-checked
description: "Host package and kernel requirements for Rook OSDs, RBD and CephFS, including when LVM is required and the imageFeatures kernel rule."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/Prerequisites/prerequisites/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LVM is required on the storage hosts only in some cases:
- encryption is enabled (`encryptedDevice: "true"` in the cluster CR)
- a metadata device is specified
- `osdsPerDevice` is greater than 1

It is not needed for OSDs on raw devices, raw partitions or PVC-based `storageClassDeviceSets`. When required, install `lvm2` on all storage nodes (`yum install -y lvm2` or `apt-get install -y lvm2`). Without it, OSDs are created but fail to start after the node reboots.

A running udev daemon is required on all storage nodes. Rook mounts `/run/udev` from the host into OSD pods and ceph-volume uses it to identify devices.

Kernel rules:
- Ceph needs the RBD module. Test with `modprobe rbd`; if it is not found, rebuild the kernel, upgrade or switch distribution. GKE Container-Optimised OS lacks RBD.
- Rook's default RBD configuration sets only the `layering` image feature for old-kernel compatibility. On kernel 5.4 or later you may use `imageFeatures: layering,fast-diff,object-map,deep-flatten,exclusive-lock` in the storage class.
- For CephFS RWX volumes the recommended minimum kernel is 4.17. Below that, PVC sizes are not enforced, because quotas need a newer kernel.

## Checked

2026-11-03. Confirmed against the Prerequisites page: when LVM is required, the udev requirement, the RBD module, imageFeatures on kernel 5.4 or later and the kernel 4.17 CephFS recommendation. Removed: nothing.

Method: documentation only; no commands were run.
