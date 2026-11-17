---
id: computing-software.cloud-infrastructure-engineering.rook.cephfs-filesystem-create-and-mds-status
name: cephfs-filesystem-create-and-mds-status
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephfilesystem, shared-filesystem, mds, standby-replay, storageclass, filesystem-yaml]
level: intro
status: docs-checked
description: "Create a shared CephFilesystem with replicated metadata and data pools, confirm MDS pods and standby-replay status, then create the CephFS StorageClass."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Shared-Filesystem-CephFS/filesystem-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A shared filesystem can be mounted read-write by many pods, which suits applications that cluster over a shared filesystem. The guide's example runs one for kube-registry on a Rook cluster from the quickstart.

Define the metadata pool, data pools and MDS in a `CephFilesystem` CR. The example uses replication 3 for the metadata pool and for a single data pool. Save as `filesystem.yaml` and run:
```
kubectl create -f filesystem.yaml
kubectl -n rook-ceph get pod -l app=rook-ceph-mds
```
The operator creates all pools and resources, which may take a minute. Two MDS pods appear, for example `rook-ceph-mds-myfs-...`.

In the toolbox, `ceph status` shows the mds line, for instance one active instance up and one in standby-replay for failover:
```
mds: myfs-1/1/1 up {[myfs:0]=mzw58b=up:active}, 1 up:standby-replay
```

Before provisioning, create a StorageClass based on the filesystem so Kubernetes can use the CSI driver to create persistent volumes (`deploy/examples/csi/cephfs/storageclass.yaml`).

The sample needs OSDs on three different nodes because both pools use `failureDomain: host` and `replicated.size: 3`. The failure domain can be another type, such as rack, if it is present in the storage selection settings.

## Checked

2026-11-03. Confirmed against the Filesystem Storage page: the CephFilesystem example with replicated size 3 pools, the rook-ceph-mds pod listing with two MDS pods, standby-replay in ceph status, the StorageClass step and the three-node failureDomain host requirement. Removed: the "about a minute" wording was aligned to the page ("may take a minute").

Method: documentation only; no commands were run.
