---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulsets-and-persistent-storage
name: statefulsets-and-persistent-storage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, persistentvolume, persistentvolumeclaim, pv, pvc, storageclass, csi, volumeclaimtemplates, headless-service, ordinal, podmanagementpolicy, reclaimpolicy, waitforfirstconsumer, allowvolumeexpansion, volumesnapshot, velero, access-modes, readwriteonce, readwriteoncepod, readwritemany, ebs, persistent-disk, operators, databases-on-kubernetes, partition-rollout]
level: advanced
status: docs-checked
description: "Run stateful workloads: StatefulSet identity and ordering, volumeClaimTemplates, StorageClass choices, reclaim policy, expansion, snapshots, and when to use an operator."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/", "https://kubernetes.io/docs/concepts/storage/storage-classes/", "https://kubernetes.io/docs/concepts/storage/volume-snapshots/", "https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/", "https://github.com/vmware-tanzu/velero"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StatefulSets and persistent storage — keeping data through every restart

**Goal:** stateful pods keep stable identity and their own disk, storage survives deletes
you did not mean, volumes can grow and be restored, and you know when not to hand-roll it.

## 1. What a StatefulSet gives you (and a Deployment does not)
- **Stable names**: `db-0`, `db-1`, … and stable DNS `db-0.db-headless.<ns>.svc` via a
  required **headless Service** (`clusterIP: None`, named in `spec.serviceName`).
- **Per-pod volumes** from `volumeClaimTemplates`: PVC `data-db-0` follows `db-0` across
  reschedules.
- **Ordering**: `OrderedReady` creates 0→N and deletes N→0, each waiting for Ready.
  `podManagementPolicy: Parallel` drops that for apps that coordinate themselves (faster
  scale-up). For rolling updates it only matters when
  `updateStrategy.rollingUpdate.maxUnavailable` is greater than 1, when the controller may update
  several pods at once (so pods can become ready out of order).
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata: {name: db}
spec:
  serviceName: db-headless
  replicas: 3
  selector: {matchLabels: {app: db}}
  updateStrategy: {type: RollingUpdate, rollingUpdate: {partition: 0}}
  persistentVolumeClaimRetentionPolicy: {whenDeleted: Retain, whenScaled: Retain}
  template:
    metadata: {labels: {app: db}}
    spec:
      terminationGracePeriodSeconds: 120      # let the DB flush and step down
      containers:
      - name: db
        image: registry.example.com/db@sha256:<DIGEST>
        volumeMounts: [{name: data, mountPath: /var/lib/db}]
  volumeClaimTemplates:
  - metadata: {name: data}
    spec: {accessModes: [ReadWriteOnce], storageClassName: fast-ssd, resources: {requests: {storage: 100Gi}}}
```

## 2. StorageClass decisions
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: fast-ssd}
provisioner: ebs.csi.aws.com          # or pd.csi.storage.gke.io, disk.csi.azure.com
parameters: {type: gp3}
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```
- **`WaitForFirstConsumer`**: provision in the zone where the pod is scheduled. `Immediate`
  can create the disk in a zone with no capacity for the pod → stuck Pending.
- **`reclaimPolicy: Retain`** for anything you cannot regenerate; the default for most
  dynamic classes is `Delete`, which destroys the cloud disk when the PVC is deleted.
- Access modes: block disks are `ReadWriteOnce` (one *node*, not one pod);
  `ReadWriteOncePod` (stable since Kubernetes 1.29, CSI volumes only) restricts the volume to a
  single pod. `ReadWriteMany` needs a backend that supports it (a network file system); do not
  put databases on a network share unless the database vendor documents support for it.

## 3. Lifecycle operations
- **Resize**: edit each PVC's `spec.resources.requests.storage` up (shrinking is not
  supported), which requires `allowVolumeExpansion: true` on the StorageClass and a CSI driver
  that supports expansion. File system expansion happens when a pod starts or while it runs if the
  file system supports online expansion; check the PVC conditions with `kubectl describe pvc`.
  The StatefulSet docs do not describe propagating a new size from `volumeClaimTemplates` to
  existing PVCs, so patch existing PVCs individually and check your Kubernetes version's notes
  before relying on template changes for new replicas.
- **Staged rollout**: set `partition: 2` so only `db-2` updates; verify, then lower the
  partition. Pods with ordinal < partition stay on the old revision.
- **Stuck rollout**: with `OrderedReady`, a broken new revision that never becomes Ready
  blocks forever — even after you fix the template you may need to delete the stuck pod
  manually (documented StatefulSet behaviour).
- **Scale down** does not delete PVCs by default; scaling back up reattaches old data
  (stale replicas may need resync).

## 4. Backups
- `VolumeSnapshot` with a `VolumeSnapshotClass` snapshots CSI volumes; it needs a CSI driver that
  implements snapshots plus the snapshot controller and CRDs, and restore is by creating a PVC
  with `dataSource: {kind: VolumeSnapshot, name: ...}`.
- A disk snapshot is not automatically application-consistent: quiesce the application or use the
  database's native backup tooling for anything transactional.
- Velero backs up and restores cluster resources and persistent volumes. A backup you have
  not restored is a hypothesis.

## 5. Operator or hand-rolled?
Prefer a mature operator for your database or a managed service: failover, replica rebuild,
backups and version upgrades are the hard part, and a StatefulSet does none of them. Hand-roll
only simple single-writer state.

## Gotchas
- Deleting a namespace deletes its PVCs; with `reclaimPolicy: Delete`, the data goes too.
- A PV in `Released` state does not rebind to a new PVC automatically; clear `spec.claimRef`.
- Node failure: a pod on an unreachable node is not deleted automatically, so the replacement
  waits; StatefulSets provide at-most-one semantics per identity. Force deletion can violate that
  and, in quorum-based systems, lead to split brain and data loss, so investigate before
  `kubectl delete pod --force`.
- `fsGroup` on large volumes causes slow recursive chown at mount; use
  `fsGroupChangePolicy: OnRootMismatch`.
- `persistentVolumeClaimRetentionPolicy` is beta and on by default from Kubernetes 1.27 and
  stable from 1.32 (`StatefulSetAutoDeletePVC`); before 1.27 the PVCs are always retained.

## Verify
- [ ] `kubectl delete pod db-1` → new `db-1` mounts the same PVC with data intact.
- [ ] StorageClass is `Retain` + `WaitForFirstConsumer` + `allowVolumeExpansion: true`.
- [ ] A PVC resize completes online without pod restart (or the need for one is documented).
- [ ] A snapshot or native backup has been restored into a fresh namespace and queried.
- [ ] `partition`-staged update rehearsed on staging.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; v1.37 latest release): StatefulSet, Persistent Volumes, Storage Classes, Volume Snapshots, force-deleting StatefulSet pods, security context pages and feature-gate stage pages; Velero README (main). Confirmed: stable pod names and per-pod PVCs, OrderedReady default and Parallel behaviour including `maxUnavailable`, `partition` semantics, `persistentVolumeClaimRetentionPolicy` stages (beta 1.27, stable 1.32), `ReadWriteOncePod` stable in 1.29, StorageClass `reclaimPolicy` default Delete and `WaitForFirstConsumer`, PVC expansion rules and no shrinking, Released PV and `claimRef`, `fsGroupChangePolicy: OnRootMismatch`, at-most-one semantics and force-delete risk, snapshot prerequisites, Velero scope. Fixed: Parallel was described as not affecting rolling updates; the retention policy version note. Removed as unconfirmed: the claims about editing `volumeClaimTemplates`, "crash-consistent" snapshots, the named operators and backup tools.

Method: documentation only; no commands were run.
