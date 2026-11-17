---
id: computing-software.cloud-infrastructure-engineering.rook.rook-storage-architecture-overview
name: rook-storage-architecture-overview
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [architecture, operator, ceph-csi, mds, not-in-data-path]
level: intro
status: docs-checked
description: "How the Rook operator, Ceph-CSI and Ceph daemons fit together and how block, shared filesystem and object storage are exposed to applications."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/storage-architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook runs Ceph on Kubernetes using Kubernetes primitives. The operator is a small container holding what is needed to bootstrap and monitor the cluster. It starts and monitors the Ceph mon pods, the OSD daemons providing RADOS storage and other Ceph daemons, and manages CRDs for pools, object stores (S3 or Swift) and filesystems.

It also watches the cluster: mons are started or failed over when needed, and it adjusts as the cluster grows or shrinks. It applies desired-state changes made in the Ceph custom resources.

Rook is not in the Ceph data path. Ceph concepts such as placement groups and CRUSH maps are hidden behind terms of physical resources, pools, volumes, filesystems and buckets, and advanced configuration can still be applied with Ceph tools. Rook automatically configures the Ceph-CSI driver, which mounts storage into pods. The rook/ceph image contains the tools to manage the cluster.

Three storage types are shown:
- Block: a ReadWriteOnce (RWO) volume mounted in one application, with Ceph managing the IO.
- Shared filesystem: a ReadWriteMany (RWX) volume shared by several applications, with the MDS daemon protecting data for multiple writers.
- Object: buckets read and written with a standard S3 client.

The diagram layers are the Rook operator, the CSI plugins and provisioners, and the Ceph daemons.

## Checked

2026-11-08. Read in full against https://rook.io/docs/rook/latest-release/Getting-Started/storage-architecture/ : operator role, not in the data path, block RWO, shared filesystem RWX with MDS, object S3, diagram layers. Nothing else was removed.

Method: documentation only; no commands were run.
