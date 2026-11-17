---
id: computing-software.cloud-infrastructure-engineering.rook.rook-cluster-teardown-and-cleanup-policy
name: rook-cluster-teardown-and-cleanup-policy
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cleanup, cleanuppolicy, teardown, zap-disk, sgdisk, yes-really-destroy-data]
level: advanced
status: docs-checked
description: "Tear down a Rook cluster safely: delete consumers first, set cleanupPolicy confirmation, delete the CephCluster, then remove operator resources and zap disks."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/ceph-teardown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Order matters. Delete applications and their PVCs, pools and storage classes before removing the cluster, otherwise volumes may hang and nodes may need a restart.

Things to clean: the rook-ceph namespace resources, every file under `dataDirHostPath` (default `/var/lib/rook`) and the OSD devices.

To have Rook wipe host paths and disks, patch the CephCluster first:
```
kubectl -n rook-ceph patch cephcluster rook-ceph --type merge \
  -p '{"spec":{"cleanupPolicy":{"confirmation":"yes-really-destroy-data"}}}'
kubectl -n rook-ceph delete cephcluster rook-ceph
kubectl -n rook-ceph get cephcluster
```
Once the policy is set, further CephCluster changes are blocked until deletion is requested, so the patch can still be reverted. After deletion, wait for the `rook-ceph-cleanup` jobs on all nodes; they delete files under `dataDirHostPath` and wipe the OSD drives. The jobs may not start if resources on top of the cluster remain.

Then delete the CSI operator resources (`operatorconfigs`, `drivers`, `clientprofiles`, `clientprofilemappings`, `cephconnections` of `csi.ceph.io`), and run `kubectl delete -f operator.yaml`, `common.yaml`, `crds.yaml`.

Without the cleanup policy, delete `dataDirHostPath` contents manually on each host. Zap a disk with `sgdisk --zap-all $DISK` and the documented `dd` or `blkdiscard` wipes, then `partprobe`. Remove leftover `/dev/mapper/ceph-*` devices with `dmsetup`; a reboot often frees disks that stay locked.

## Checked

2026-11-03. Confirmed against the Cleanup page: the delete order, the cleanupPolicy confirmation patch, the rook-ceph-cleanup jobs, the CSI resource kinds, and the sgdisk, dd, blkdiscard, partprobe and dmsetup steps. Removed: nothing.

Method: documentation only; no commands were run.
