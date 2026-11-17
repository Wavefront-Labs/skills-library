---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-volume-snapshots
name: mayastor-volume-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, snapshot, copy-on-write, csi-snapshot-controller, immutability, incremental, helm]
level: practitioner
status: docs-checked
description: "Mayastor volume snapshots: incremental COW read-only copies, consistency, create and delete flow, capacity thresholds, and disabling the bundled csi-snapshot-controller."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/volume-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replicated PV Mayastor supports industry-standard **copy-on-write snapshots**, tracking changed blocks. They are read-only, incremental copies of a volume at a point in time, and the docs present them as helpful for migrating or moving data between clusters, clouds or data centres.

Documented use cases: efficient replication for backups, clones for troubleshooting, and developing against a read-only copy of the data.

Properties:

- **Consistency**: the data in a snapshot is consistent across all replicas of the volume, local or remote.
- **Immutability**: once successfully created, the content cannot change.
- **No rebuild**: unlike volume replicas, snapshots cannot be rebuilt after a node failure.

Supported operations: create a snapshot for a PVC, list snapshots for a PVC, and delete a snapshot for a PVC.

Prerequisites: install and configure Replicated PV Mayastor and create disk pools; have a PVC in the Bound state (the guide uses `ms-volume-claim`); and run an application on it per the deployment guide.

**Snapshot controller.** Mayastor runs a `csi-snapshot-controller` container by default. A cluster should only run one, so if the cluster already manages one, disable the bundled controller by setting `mayastor.csi.controller.snapshotController.enabled` to `false` in the Helm chart values.

**Create flow.** Create a VolumeSnapshotClass with driver `io.openebs.csi-mayastor` and `deletionPolicy: Delete` (the example marks it default with the `snapshot.storage.kubernetes.io/is-default-class: "true"` annotation), then a VolumeSnapshot whose `volumeSnapshotClassName` names that class and whose `source.persistentVolumeClaimName` is the PVC. List with `kubectl get volumesnapshot` and `kubectl get volumesnapshotcontent`; delete with `kubectl delete volumesnapshot <name>`. Snapshotting a thick-provisioned volume converts it to thin.

**Filesystem consistency.** By default snapshots are filesystem consistent: the csi-node plugin runs the FIFREEZE and FITHAW ioctls around the snapshot, and a failure of any step fails the process, which the CSI controller retries without user action. The page disables this through a VolumeSnapshotClass parameter (the text says `quiesceFS`, the example uses `quiesceFs: none`).

**Capacity thresholds.** Snapshot creation is checked per replica pool against Helm values under `mayastor.agents.core.capacity.thin`: `poolCommitment` 250%, `volumeCommitment` 40%, `volumeCommitmentInitial` 40% and `snapshotCommitment` 40% by default. With snapshotCommitment 40% and a 100 GiB volume, each replica pool needs 40 GiB free or snapshot creation fails. A thick volume that gets converted to thin raises the pool's committed capacity by the volume size, which can also trip the limits.

## Checked

Method: 2026-11-08 read the raw markdown of the Mayastor volume snapshots guide (the published volume-snapshots page, file name snapshot.md) in full. Original claims match. Removed a pointer to another skill and a replica-snapshot remark this page does not state, and added the create flow, filesystem-consistency and capacity-threshold sections the page does state.
