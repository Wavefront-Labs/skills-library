---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volume-snapshots-and-cloning
name: volume-snapshots-and-cloning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volumesnapshot, volumesnapshotclass, volumesnapshotcontent, csi-snapshotter, pvc-clone, datasource, clone-pvc, crash-consistent, application-consistent, restore, snapshot-controller]
level: advanced
status: docs-checked
description: "VolumeSnapshot/VolumeSnapshotClass CRDs end to end: taking a snapshot, restoring into a new PVC, PVC-to-PVC cloning, and where crash-consistent isn't enough."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-snapshots/", "https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/", "https://kubernetes-csi.github.io/docs/volume-cloning.html", "https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume snapshots and cloning — point-in-time copies without leaving Kubernetes

**Goal:** take a snapshot, restore it into a fresh PVC, clone a live PVC directly, and
know when any of that is not enough for a transactional workload.

## 1. The three CRDs (CRDs, not part of the core API; the distribution installs them and the snapshot controller — check `kubectl api-resources | grep snapshot`)
- `VolumeSnapshotClass` — names a `driver` (must match the CSI driver) and `deletionPolicy` (`Delete` or
  `Retain`; required). `Delete` deletes the underlying storage snapshot along with the content object.
- `VolumeSnapshot` — namespaced request for a snapshot, with `source.persistentVolumeClaimName` for dynamic provisioning.
- `VolumeSnapshotContent` — cluster-scoped; created by the snapshot controller for dynamic snapshots and bound
  one-to-one to a `VolumeSnapshot`; `status.snapshotHandle` is the backend snapshot ID.
  Snapshots work only with CSI drivers that implement them (csi-snapshotter sidecar).

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata: {name: csi-snap}
driver: ebs.csi.aws.com
deletionPolicy: Retain
---
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata: {name: db-snap-2026-10-15}
spec:
  volumeSnapshotClassName: csi-snap
  source: {persistentVolumeClaimName: db-data-db-0}
```
Wait for `kubectl get volumesnapshot db-snap-2026-10-15 -o jsonpath='{.status.readyToUse}'`
to be `true` (readyToUse means the snapshot can be used to restore a volume) before trusting it.

## 2. Restoring a snapshot into a PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: db-restored}
spec:
  storageClassName: fast-ssd
  dataSource: {name: db-snap-2026-10-15, kind: VolumeSnapshot, apiGroup: snapshot.storage.k8s.io}
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 100Gi}}   # at least the snapshot's status.restoreSize
```
This provisions a new volume pre-populated from the snapshot; the original PVC is untouched.
Mount it on a scratch pod and verify data before pointing production at it.

## 3. PVC-to-PVC cloning (no snapshot object at all)
```yaml
spec:
  dataSource: {name: db-data-db-0, kind: PersistentVolumeClaim}
  storageClassName: fast-ssd   # may be the same or a different class than the source; omitting it uses the default class
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 100Gi}}
```
Cloning is a separate CSI driver capability (`CLONE_VOLUME`) from snapshot support: drivers may or may
not implement it, so check the driver's documentation. The documented rules: CSI drivers and dynamic provisioners only;
the source PVC must be bound and not in use; source and destination must be in the **same namespace**;
the destination may use the same or a different StorageClass; both must use the same VolumeMode; the
requested size must be the same or larger than the source. Cross-namespace data sources are alpha (since 1.26) and need
`CrossNamespaceVolumeDataSource` plus a ReferenceGrant; see
`computing-software.cloud-infrastructure-engineering.kubernetes.volume-populators-datasourceref`.

## 4. Crash-consistent vs. application-consistent
A CSI volume snapshot copies the volume, not the application's in-memory state: treat a plain snapshot as
crash-consistent at best, and use the application's own backup or quiesce mechanism when you need
application-consistent data. Multi-volume applications should be snapshotted together with a
`VolumeGroupSnapshot` (group snapshots represent copies of multiple volumes taken at the same point in time;
only drivers that implement the group snapshot capability support it; see
`computing-software.cloud-infrastructure-engineering.kubernetes.volumegroupsnapshot-crash-consistency`).

## Gotchas
- A PVC that is in active use as a snapshot source is not removed immediately; removal is postponed until the
  snapshot is readyToUse or aborted.
- With `deletionPolicy: Delete`, deleting the `VolumeSnapshot` deletes the backend snapshot too; use `Retain` for
  snapshots you rely on for disaster recovery (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.volumesnapshot-deletion-policy`).
- Check the CSI driver's documentation for restore performance characteristics; the Kubernetes docs do not promise instant restores.

## Verify
- [ ] Took a snapshot, confirmed `readyToUse: true`, restored it into a new PVC in a
      scratch pod, and verified the data.
- [ ] Cloned a PVC directly (no snapshot step) and confirmed the same-namespace and same-VolumeMode rules.
- [ ] Named whether the workload's snapshot is crash-consistent or
      application-consistent, and what compensates if it's only the former.
- [ ] Checked `deletionPolicy` on the `VolumeSnapshotClass` before relying on
      snapshots for disaster recovery.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: the snapshot CRDs and who installs them, deletionPolicy semantics, readyToUse and restoreSize meanings, PVC-as-snapshot-source protection, cloning rules (same namespace, different StorageClass allowed, same VolumeMode, size >= source, source bound and not in use), CLONE_VOLUME as a driver capability. Corrected two wrong claims: cloning does not require the same StorageClass, and restoring a snapshot into a different namespace is not supported by the core `dataSource` (cross-namespace is the alpha `dataSourceRef` mechanism). Also corrected the restore size rule (restoreSize, not source size) and removed the claim that a CSIDriver object lists capabilities, the PV-style phase analogy, lazy hydration, class-deletion and database tool names.

Method: documentation only; no commands were run.
