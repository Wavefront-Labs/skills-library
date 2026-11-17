---
id: computing-software.cloud-infrastructure-engineering.rook.cephblockpoolradosnamespace-multitenancy
name: cephblockpoolradosnamespace-multitenancy
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephblockpoolradosnamespace, rados-namespace, multi-tenancy, clusterid, blockpoolname]
level: practitioner
status: docs-checked
description: "Create RADOS namespaces inside a CephBlockPool for tenant isolation, with clusterID and namespace-level mirroring settings."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Block-Storage/ceph-block-pool-rados-namespace-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RADOS pools serve both data distribution (pools split into PGs that map to OSDs) and security granularity (capabilities can restrict access by pool). Overloading pools this way makes multi-tenancy awkward, since very many pools is not a good idea.

A RADOS namespace divides a pool into separate logical namespaces. Several Kubernetes clusters can then share one Ceph cluster without a pool per cluster, and tenants in one Kubernetes cluster can be isolated without a pool per tenant. Rook creates them through the `CephBlockPoolRadosNamespace` CRD, for example on the pool `replicapool` in namespace `rook-ceph`.

Fields:
- `name`: the name of the rados namespace.
- `blockPoolName`: the metadata name of the CephBlockPool CR where the namespace is created.
- `clusterID`: the ID used for this namespace in the CSI configuration; Rook generates one if unset.
- `mirroring` (requires Ceph v20 or newer):
  - `mode`: `pool` or `image` (required).
  - `remoteNamespace`: the namespace name on the peer; default is the same name.
  - `snapshotSchedules`: one or more, each with an `interval` using d, h or m suffixes and an optional `startTime`.

Mirroring peers are configured individually per CephBlockPoolRadosNamespace. Disabling mirroring on a CephBlockPool requires first disabling it on every namespace under it.

## Checked

2026-11-03. Confirmed against the CephBlockPoolRadosNamespace CRD page: the name, blockPoolName, clusterID and mirroring (mode, remoteNamespace, snapshotSchedules) fields, the Ceph v20 mirroring requirement, and per-namespace peers. Removed: nothing.

Method: documentation only; no commands were run.
