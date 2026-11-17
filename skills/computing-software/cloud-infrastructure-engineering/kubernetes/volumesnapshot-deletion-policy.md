---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volumesnapshot-deletion-policy
name: volumesnapshot-deletion-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volumesnapshot, snapshot-deletionpolicy, volumesnapshotclass, backups]
level: practitioner
status: docs-checked
description: "Choose VolumeSnapshotClass deletionPolicy Delete or Retain, how it propagates to VolumeSnapshotContent, and protecting backend snapshots from accidental deletion."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-snapshots/#delete", "https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/#deletionpolicy", "https://github.com/kubernetes-csi/external-snapshotter/blob/master/client/apis/volumesnapshot/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VolumeSnapshot deletionPolicy

Three objects: `VolumeSnapshot` (namespaced request), `VolumeSnapshotContent` (cluster-scoped,
points at the real backend snapshot), `VolumeSnapshotClass` (driver + policy).

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata: {name: ebs-retain}
driver: ebs.csi.aws.com
deletionPolicy: Retain      # or Delete
```

## Semantics
- `Delete`: deleting the VolumeSnapshot deletes the content object AND the backend snapshot.
- `Retain`: deleting the VolumeSnapshot leaves both the content object and the backend snapshot; the content's
  `status.snapshotHandle` identifies the backend snapshot.
- For dynamically provisioned snapshots the content's `deletionPolicy` is filled in by the csi-snapshotter sidecar
  from the VolumeSnapshotClass; for pre-existing snapshots you must set it when creating the VolumeSnapshotContent.
  The field is not marked immutable in the API, so you can patch it on an existing content object:
```bash
kubectl patch volumesnapshotcontent snapcontent-1234 --type merge -p '{"spec":{"deletionPolicy":"Retain"}}'
```

## When to use which
- Short-lived snapshots for clones or CI: Delete, so the backend snapshot is removed with the object.
- Snapshots you rely on as backups: Retain, so deleting the VolumeSnapshot does not delete the backend snapshot
  (you then manage expiry on the storage side).
- Backup tools that manage snapshot objects: follow their documentation.

## Cleanup of retained snapshots
```bash
kubectl get volumesnapshotcontent -o custom-columns=NAME:.metadata.name,POLICY:.spec.deletionPolicy,SNAP:.spec.volumeSnapshotRef.name,HANDLE:.status.snapshotHandle
```
A retained content object whose VolumeSnapshot is gone keeps the backend snapshot; to remove it, delete it on
the storage side, or set the policy to Delete and then delete the content object (with `Delete`, the underlying
snapshot is deleted along with the content object).

## Gotchas
- Deleting a VolumeSnapshot (including by deleting its namespace) with a `Delete` policy deletes the backend snapshot.
- A PVC that is the source of an in-progress snapshot is protected from removal until the snapshot is readyToUse or aborted.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: Delete and Retain semantics (Kubernetes docs), VolumeSnapshotClass deletionPolicy required with values Retain or Delete, content deletionPolicy filled from the class for dynamic snapshots and required for pre-existing ones, no immutable marker on the content field, status.snapshotHandle (snapshot.storage.k8s.io/v1 types), PVC-as-source protection. Removed the unconfirmed Velero statement and the claim about snapshot finalizers blocking deletion while a snapshot is a PVC data source.

Method: documentation only; no commands were run.
