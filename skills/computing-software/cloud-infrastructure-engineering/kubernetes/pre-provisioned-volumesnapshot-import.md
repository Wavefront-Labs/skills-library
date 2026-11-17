---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pre-provisioned-volumesnapshot-import
name: pre-provisioned-volumesnapshot-import
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-snapshots, pre-provisioned-snapshot, volumesnapshotcontent, disaster-recovery]
level: practitioner
status: docs-checked
description: "Import an existing cloud disk snapshot into Kubernetes with a static VolumeSnapshotContent and VolumeSnapshot pair, then restore a PVC from it."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-snapshots/#pre-provisioned-snapshot", "https://github.com/kubernetes-csi/external-snapshotter", "https://github.com/kubernetes-csi/external-snapshotter/blob/master/client/apis/volumesnapshot/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing pre-provisioned snapshots

Use this to restore a snapshot made outside the cluster (another cluster, a backup tool, or the
cloud console).

## 1. VolumeSnapshotContent pointing at the real snapshot
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotContent
metadata: {name: imported-db-snap}
spec:
  deletionPolicy: Retain                 # Retain keeps the underlying snapshot and this object on deletion
  driver: ebs.csi.aws.com
  source:
    snapshotHandle: snap-0123456789abcdef0
  sourceVolumeMode: Filesystem
  volumeSnapshotClassName: ebs-snapclass
  volumeSnapshotRef:
    name: db-snap
    namespace: data
```

## 2. VolumeSnapshot bound to that content
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata: {name: db-snap, namespace: data}
spec:
  source:
    volumeSnapshotContentName: imported-db-snap
```

## 3. Restore
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: db-restored, namespace: data}
spec:
  storageClassName: gp3
  dataSource: {apiGroup: snapshot.storage.k8s.io, kind: VolumeSnapshot, name: db-snap}
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 100Gi}}      # at least the snapshot's status.restoreSize
```

## Gotchas
- `volumeSnapshotRef` in the VolumeSnapshotContent names the VolumeSnapshot (name and namespace); that
  VolumeSnapshot might not exist yet when the content is created. `snapshotHandle` is the
  snapshot's ID on the storage backend and is required for pre-provisioned snapshots.
- Whether a snapshot on the backend is usable from your cluster is a storage-side question; consult the CSI driver's documentation.
- For pre-provisioned snapshots the cluster administrator must populate `sourceVolumeMode` (`Filesystem` or
  `Block`); restoring with a different volume mode than the source requires the annotation
  `snapshot.storage.kubernetes.io/allow-volume-mode-change: "true"` on the VolumeSnapshotContent.

## Verify
```bash
kubectl get volumesnapshot db-snap -n data -o jsonpath='{.status.readyToUse} {.status.restoreSize}'
```
`status.readyToUse` is `true` and `status.restoreSize` (the minimum size of volume needed to restore) is set; then the PVC can be created from the snapshot.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed against the Volume Snapshots concepts page and the snapshot.storage.k8s.io/v1 types: field names (deletionPolicy, driver, source.snapshotHandle, sourceVolumeMode, volumeSnapshotClassName, volumeSnapshotRef), volumeSnapshotContentName on the VolumeSnapshot, restoreSize meaning, deletionPolicy Retain semantics, and the allow-volume-mode-change annotation. Removed the unconfirmed 'neither becomes ready' claim and the cross-region/account instruction.

Method: documentation only; no commands were run.
