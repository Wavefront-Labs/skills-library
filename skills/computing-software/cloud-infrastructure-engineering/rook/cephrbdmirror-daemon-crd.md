---
id: computing-software.cloud-infrastructure-engineering.rook.cephrbdmirror-daemon-crd
name: cephrbdmirror-daemon-crd
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephrbdmirror, rbd-mirror, count, placement, priorityclassname, asynchronous-replication]
level: practitioner
status: docs-checked
description: "Deploy rbd-mirror daemons through the CephRBDMirror CRD and understand where peers are configured for pools and rados namespaces."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Block-Storage/ceph-rbd-mirror-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook creates and updates rbd-mirror daemons through the `CephRBDMirror` CRD. RBD images can be asynchronously mirrored between two Ceph clusters. The guide assumes a Rook cluster from the quickstart. Any unspecified setting uses a default.

Fields:
- `name`: the name of the Ceph RBD Mirror daemon resource.
- `namespace`: the Kubernetes namespace of the Rook cluster; the services and pods created by the operator are added there.
- `count`: how many rbd-mirror instances to run.
- `placement`: standard Kubernetes restrictions (`nodeAffinity`, `tolerations`, `podAffinity`, `podAntiAffinity`), like daemons in the cluster CRD.
- `annotations` and `labels`: key-value lists added to the pods.
- `resources`: resource requirements for the mirror pods.
- `priorityClassName`: priority class for the pods.

Mirroring peers are not set on this CR. Configure peers individually for each CephBlockPool, and individually for each CephBlockPoolRadosNamespace; see those pages. Pool-level mirroring (`mirroring.enabled`, `mode`, `snapshotSchedules`) and the bootstrap peer token are described in the CephBlockPool skill.

## Checked

2026-11-03. Confirmed against the CephRBDMirror CRD page: the name, namespace, count, placement, annotations, labels, resources and priorityClassName fields and that peers are set per CephBlockPool and per CephBlockPoolRadosNamespace. Removed: the self-check paragraph, which the page does not state.

Method: documentation only; no commands were run.
