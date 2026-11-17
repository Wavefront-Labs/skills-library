---
id: computing-software.cloud-infrastructure-engineering.rook.rook-application-migration-between-clusters
name: rook-application-migration-between-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [application-migration, external-cluster, persistent-volume, claimref, velero, retain]
level: advanced
status: docs-checked
description: "Move applications between Kubernetes clusters that share one external Ceph cluster by saving the PV and recreating it, with no data movement."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/app-migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When several Kubernetes clusters connect to the same external Ceph cluster, the applications store data centrally, so an application can move to another cluster without moving data. This helps when a cluster is overloaded or has an outage. The docs example has App A with an RBD RWO PVC and App B with a CephFS RWX PVC in cluster 1.

Requirements:
- One external Ceph cluster reachable from the application clusters, configured by Rook with host networking or by tools like cephadm.
- Application clusters connected to the same external cluster with access to the same pool, radosnamespace (RBD) and/or subvolumegroup (CephFS).

Preparing each application:
1. Create the application and PVC in the first cluster.
2. Find the bound PV, for example `kubectl get pvc rbd-pvc -o yaml | grep volumeName`.
3. Save it without identity fields:
```
kubectl get pv pvc-<id> -o yaml | egrep -v " uid: | resourceVersion: " > application-pv.yaml
```
Tools such as Velero can back up the PV instead.

Migrating: scale down the application in the first cluster. For an RWO PVC make sure the application is stopped and cannot reach Ceph by accident, since RBD volumes have no protection against corruption from two writers. Then create the PV and PVC in the second cluster and start the application there.

Tip: provision from a storage class with `reclaimPolicy: Retain` so deleting a volume in one cluster does not remove it while another cluster uses it.

## Checked

2026-11-03. Confirmed against the Application Migration page: the requirements, the PV save command, scale down and RWO corruption warning, and the Retain reclaimPolicy tip. Removed: nothing.

Method: documentation only; no commands were run.
