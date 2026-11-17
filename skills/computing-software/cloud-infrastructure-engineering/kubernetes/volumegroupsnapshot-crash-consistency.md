---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volumegroupsnapshot-crash-consistency
name: volumegroupsnapshot-crash-consistency
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-snapshots, volumegroupsnapshot, crash-consistency, csi, databases]
level: practitioner
status: docs-checked
description: "Take crash-consistent snapshots of several PVCs at once with VolumeGroupSnapshot, and restore an application whose data and logs live on separate volumes."
sources: ["https://kubernetes-csi.github.io/docs/group-snapshot-restore-feature.html", "https://kubernetes-csi.github.io/docs/external-snapshotter.html", "https://kubernetes-csi.github.io/docs/snapshot-controller.html", "https://github.com/kubernetes-csi/external-snapshotter/tree/master/examples/kubernetes", "https://kubernetes.io/docs/concepts/storage/volume-snapshots/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VolumeGroupSnapshot

Snapshotting PVCs one by one gives slightly different points in time; a database with data and
WAL on separate volumes may not recover. VolumeGroupSnapshot asks the storage to cut all of them
at the same point in time. The kubernetes-csi docs list it as beta since Kubernetes 1.32 (alpha 1.27 to 1.32).

## Prerequisites
- Group snapshot CRDs (`groupsnapshot.storage.k8s.io`), installed by the distribution, and a snapshot-controller
  started with `--enable-volume-group-snapshots`.
- csi-snapshotter (external-snapshotter) sidecar with `--enable-volume-group-snapshots`, and a driver that
  advertises the `CREATE_DELETE_GET_VOLUME_GROUP_SNAPSHOT` group controller capability.

## Use
```yaml
apiVersion: groupsnapshot.storage.k8s.io/v1beta1     # as in the kubernetes-csi examples; check the version your CRDs serve
kind: VolumeGroupSnapshotClass
metadata: {name: csi-group}
driver: hostpath.csi.k8s.io      # the CSI hostpath example driver; use your driver's name
deletionPolicy: Delete
---
apiVersion: groupsnapshot.storage.k8s.io/v1beta1
kind: VolumeGroupSnapshot
metadata: {name: pg-0001, namespace: data}
spec:
  volumeGroupSnapshotClassName: csi-group
  source:
    selector:
      matchLabels: {snapshot-group: pg}       # label every PVC of the app
```
The group snapshot produces a VolumeSnapshot for each member PVC; those VolumeSnapshots are owned by the VolumeGroupSnapshot.

## Restore
```bash
kubectl get volumesnapshot -n data -o jsonpath='{range .items[?(@.metadata.ownerReferences[0].name=="pg-0001")]}{.metadata.name}{"\n"}{end}'
```
Create one PVC per member from its VolumeSnapshot (`dataSource`), then start the app on the new PVCs.

## Notes
A group snapshot is crash consistent: copies of the volumes taken at the same point in time. That is not
the same as application-consistent; if you need application consistency, quiesce or checkpoint the
application using its own tooling before taking the snapshot.

## Verify
`kubectl get volumegroupsnapshot pg-0001 -n data -o jsonpath='{.status.readyToUse}'` is `true`, and
a restored copy starts and passes the database's own consistency check.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed in the kubernetes-csi docs and external-snapshotter examples: group snapshot status table (alpha 1.27-1.32, beta from 1.32), --enable-volume-group-snapshots on the snapshot-controller and sidecar, CREATE_DELETE_GET_VOLUME_GROUP_SNAPSHOT, the v1beta1 VolumeGroupSnapshotClass and VolumeGroupSnapshot example shapes (spec.source.selector.matchLabels, volumeGroupSnapshotClassName), member VolumeSnapshots owned by the group, and the restore procedure via dataSource. The external-snapshotter client also ships v1beta2 and v1 APIs, so check which version your installed CRDs serve. Removed the unconfirmed label-based restore selector, the GKE driver example and the database-specific freeze commands. The old blog URL was not checked and was replaced.

Method: documentation only; no commands were run.
