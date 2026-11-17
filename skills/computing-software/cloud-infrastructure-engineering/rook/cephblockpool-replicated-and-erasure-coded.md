---
id: computing-software.cloud-infrastructure-engineering.rook.cephblockpool-replicated-and-erasure-coded
name: cephblockpool-replicated-and-erasure-coded
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephblockpool, replicated, erasurecoded, datachunks, codingchunks, failuredomain]
level: practitioner
status: docs-checked
description: "Define replicated and erasure-coded RBD pools in a CephBlockPool, with host failure domain, chunk counts, host minimums and device class."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Block-Storage/ceph-block-pool-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replicated pool: three full copies on three nodes.
```
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: replicapool
  namespace: rook-ceph
spec:
  failureDomain: host
  replicated:
    size: 3
  deviceClass: hdd
```
It needs at least one OSD on each of at least three nodes.

Erasure coded pool: `erasureCoded: {dataChunks: 4, codingChunks: 2}` with `failureDomain: host`. That is EC 4+2, doubling usable space compared with size 3, and survives any two OSDs lost. It needs at least six OSDs of the specified device class.

Rules from the page:
- `replicated` and `erasureCoded` are mutually exclusive.
- `failureDomain` is `osd` or `host` (default host), or another type such as rack if nodes carry topology labels. `osd` is strongly discouraged for valuable data. Changing it makes the operator create a new CRUSH rule.
- `codingChunks: 1` is extremely risky; production pools need at least 2.
- Use at least three nodes for replicated and four for EC; with `failureDomain: host` have at least dataChunks+1 hosts, ideally dataChunks+codingChunks+1.
- Small clusters can pick dataChunks 3 or 2 for five or four host minimums.
- `requireSafeReplicaSize: false` permits size 1, which leads to permanent data loss.

## Checked

2026-11-03. Confirmed against the CephBlockPool CRD page: replicated size 3 example, EC 4+2 with codingChunks 2 (double the usable space of size 3, survives two OSD losses, six OSDs needed), failureDomain host or osd, codingChunks 1 risk, dataChunks 3 or 2 for smaller clusters, requireSafeReplicaSize. Removed: the unsourced claims that size 3 tolerates two lost hosts and that EC costs lower write performance and longer recovery, and the generic performance remark.

Method: documentation only; no commands were run.
