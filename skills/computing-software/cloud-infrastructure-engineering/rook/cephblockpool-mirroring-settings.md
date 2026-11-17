---
id: computing-software.cloud-infrastructure-engineering.rook.cephblockpool-mirroring-settings
name: cephblockpool-mirroring-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [mirroring, snapshotschedules, bootstrap-peer-token, pool-peer-token, rbd-mirror, peers]
level: advanced
status: docs-checked
description: "Enable RBD mirroring on a CephBlockPool, set snapshot schedules and peers, and fetch the bootstrap peer token secret."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Block-Storage/ceph-block-pool-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RBD mirroring asynchronously replicates block images or whole pools between Ceph clusters, with point-in-time consistent data including resizes, snapshots, clones and flattening. It suits disaster recovery across geographically distributed clusters whose latency rules out a stretch cluster, or when client write performance matters more than zero RPO.

Enable image-level mirroring:
```
spec:
  replicated:
    size: 3
  mirroring:
    enabled: true
    mode: image
    snapshotSchedules:
    - interval: 24h
```
Fields:
- `enabled`: default false.
- `mode`: `pool`, `image` or `init-only` (required).
- `snapshotSchedules`: one or more; `interval` uses d, h or m suffixes, and `startTime` is optional ISO 8601.
- `peers.secretNames`: peers to connect to; only one peer (one Ceph cluster) is currently supported.
- `statusCheck.mirror`: status checks, with `interval` defaulting to 60s.

Once enabled, Rook creates a bootstrap peer token. The Secret name appears in the CR status (for example `pool-peer-token-replicapool`):
```
kubectl get secret -n rook-ceph pool-peer-token-replicapool -o jsonpath='{.data.token}'|base64 -d
```
The decoded result is another base64 blob to import on the destination cluster with `rbd mirror pool peer bootstrap import <token file path>`. Read the RBD Mirror CRD page first as a prerequisite.

Disabling mirroring on the pool requires first disabling it on every CephBlockPoolRadosNamespace beneath it.

## Checked

2026-11-03. Confirmed against the CephBlockPool CRD page: the mirroring example, enabled default false, mode values pool/image/init-only, snapshotSchedules interval suffixes, peers.secretNames with only one peer supported, statusCheck.mirror, the rbd mirror pool peer bootstrap import step and the rule to disable namespace mirroring before the pool. Removed: nothing.

Method: documentation only; no commands were run.
