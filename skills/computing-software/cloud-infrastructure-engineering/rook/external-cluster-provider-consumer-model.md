---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-provider-consumer-model
name: external-cluster-provider-consumer-model
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [external-cluster, provider-cluster, consumer-cluster, cephadm]
level: intro
status: docs-checked
description: "Understand Rook external mode: a provider Ceph cluster, a consumer Kubernetes cluster, and the export-then-import workflow."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/external-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An external cluster is a Ceph configuration managed outside the local Kubernetes cluster, for example by cephadm or by another Rook cluster that allows access, usually through host networking. In external mode Rook supplies the configuration for the CSI driver and other basic resources so applications can connect to that Ceph cluster.

Terms:
- Provider cluster: provides the data, usually configured by cephadm.
- Consumer cluster: the Kubernetes cluster consuming it.

Prerequisites on the provider: create the storage types you need, namely RBD pools and a CephFS filesystem.

Workflow:
1. Export config from the provider. The Ceph admin exports what is needed to connect, such as a Ceph keyring and the mon endpoints.
2. Import that config into the consumer so Rook has the connection details.

The section also covers advanced options (NFS, exporting Rook to another cluster, admin privileges, external object store) and upgrades.

## Checked

2026-11-03. Confirmed against the External Storage Cluster page: provider and consumer definitions, the cephadm or other-Rook-cluster origin, the RBD pool and CephFS prerequisites, the export then import workflow and the list of advanced option and upgrade topics. Removed: the external.enable: true paragraph (ignored options, cephVersion.image, refusal to create extra CRs) and its tag, which the cited page does not contain.

Method: documentation only; no commands were run.
