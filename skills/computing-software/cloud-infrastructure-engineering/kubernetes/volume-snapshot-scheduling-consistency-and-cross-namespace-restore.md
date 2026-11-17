---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volume-snapshot-scheduling-consistency-and-cross-namespace-restore
name: volume-snapshot-scheduling-consistency-and-cross-namespace-restore
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-snapshots, snapshot-schedule, snapscheduler, freeze-hooks, pre-snapshot-hook, cross-namespace-snapshot, csi]
level: advanced
status: docs-checked
description: "Operate CSI VolumeSnapshots: scheduled snapshots with retention, application-consistent snapshots via freeze hooks, and restoring into another namespace."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-snapshots/", "https://backube.github.io/snapscheduler/", "https://velero.io/docs/main/backup-hooks/", "https://kubernetes.io/docs/concepts/storage/volume-populators-and-data-sources/", "https://kubernetes-csi.github.io/docs/group-snapshot-restore-feature.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume snapshots: schedules, consistency, cross-namespace restore

## Scheduled snapshots with retention
Kubernetes itself has no snapshot schedule. Options include SnapScheduler (backube), whose `SnapshotSchedule` is namespaced:
```yaml
apiVersion: snapscheduler.backube/v1
kind: SnapshotSchedule
metadata: {name: hourly, namespace: db}
spec:
  claimSelector:
    matchLabels: {backup: "true"}
  schedule: "17 * * * *"
  retention: {expires: "168h", maxCount: 10}
  snapshotTemplate:
    snapshotClassName: <snapshot-class>
    labels: {schedule: hourly}
```
The cron schedule is interpreted in UTC; pick an offset rather than `@hourly` to spread load. `maxCount` is per PVC; if both `expires` and `maxCount` are set the more restrictive wins. If `snapshotClassName` is omitted the cluster default is used.
Snapshot lifecycle follows the `deletionPolicy` of the VolumeSnapshotContent (from the VolumeSnapshotClass): with `Delete`, deleting the VolumeSnapshot deletes the underlying storage snapshot and the content object; with `Retain` both remain.

## Application-consistent snapshots
Velero runs commands in a container before and after backing up a Pod, configured by Pod annotations (commands are not run in a shell, so include `/bin/sh -c` if needed):
```yaml
metadata:
  annotations:
    pre.hook.backup.velero.io/container: postgres
    pre.hook.backup.velero.io/command: '["/bin/sh","-c","psql -U postgres -c CHECKPOINT"]'
    pre.hook.backup.velero.io/on-error: Fail
    pre.hook.backup.velero.io/timeout: 30s
    post.hook.backup.velero.io/command: '["/bin/sh","-c","<post-backup-command>"]'
```
`container` defaults to the first container, `on-error` is `Fail` or `Continue` (default `Fail`), and `timeout` defaults to 30s. Velero's own documented example freezes the filesystem with `fsfreeze --freeze` / `--unfreeze` pre and post hooks. Since Velero 1.15 related Pods are grouped into ItemBlocks: all pre hooks run, then the items are backed up, then all post hooks run.

For several volumes snapshotted together, the CSI VolumeGroupSnapshot API is beta from Kubernetes 1.32 (external-snapshotter 8.2+); it is an external snapshot-controller feature, not a core gate.

## Restore into another namespace
A PVC can restore from a VolumeSnapshot in its own namespace. Cross-namespace data sources need the alpha `CrossNamespaceVolumeDataSource` feature (since 1.26, off by default; also enabled on the csi-provisioner) and a Gateway API `ReferenceGrant` in the source namespace, using `dataSourceRef.namespace`.

Without it, a pre-provisioned snapshot in the target namespace can reference the same backing snapshot by handle:
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotContent
metadata: {name: restore-db-copy}
spec:
  deletionPolicy: Retain
  driver: <csi-driver-name>
  source: {snapshotHandle: <snapshot-handle>}
  volumeSnapshotRef: {name: db-copy, namespace: staging}
---
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata: {name: db-copy, namespace: staging}
spec:
  source: {volumeSnapshotContentName: restore-db-copy}
```
`snapshotHandle` is the identifier of the snapshot created on the storage backend; `volumeSnapshotRef` names the VolumeSnapshot and it may not exist yet. Use `Retain` so deleting the copy does not delete the original storage snapshot. Then create a PVC in the target namespace with `dataSource: {kind: VolumeSnapshot, name: db-copy, apiGroup: snapshot.storage.k8s.io}`.

## Verify
- [ ] `kubectl get volumesnapshot -A` shows `READYTOUSE` true and retention pruning old snapshots.
- [ ] A periodic restore into a scratch namespace passes application checks.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: VolumeSnapshotContent fields and deletionPolicy, SnapScheduler fields, Velero hook annotations and defaults, VolumeGroupSnapshot beta in 1.32, CrossNamespaceVolumeDataSource alpha with ReferenceGrant.

Method: documentation only; no commands were run.
