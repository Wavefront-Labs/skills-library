---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pv-pvc-binding-internals
name: pv-pvc-binding-internals
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, persistentvolume, persistentvolumeclaim, pv, pvc, binding, static-provisioning, claimref, volumename, selector, phases, pv-recycler, released, available, bound, storage-internals, pvc-selector]
level: advanced
status: docs-checked
description: "The PV/PVC binding algorithm: phases, matching rules, claimRef, static provisioning by hand, and why a Released PV won't rebind."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/", "https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/component-helpers/storage/volume/pv_helpers.go"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PV/PVC binding internals — what the binder actually checks

**Goal:** read `kubectl get pv,pvc` phases correctly, hand-provision a PV, and unstick a
binding that "should" work but doesn't.

## 1. The phases
- **PVC**: `Pending` -> `Bound`; `Lost` when its PV has disappeared.
- **PV**: `Available` -> `Bound` -> `Released` (claim deleted, storage not yet reclaimed) and `Failed`
  (automated reclamation failed).
- `Released` is the trap: with `Retain` the volume is not available for another claim because the
  previous claimant's data remains on it. The binder only picks `Available` volumes for new claims.
  To reuse it, an administrator reclaims the storage manually; the docs' recovery procedure deletes the
  `claimRef` entry from the PV spec so a new PVC can bind (only do this once you have confirmed the
  data is what you expect):
  `kubectl patch pv <name> -p '{"spec":{"claimRef": null}}'`.

## 2. The matching algorithm (static binding)
For a PVC to bind to an existing PV (from the PV controller's matching code and the PV docs), the PV must be:
- `Available` (and not already `claimRef`'d to a different claim),
- of the same `storageClassName` as the claim (empty string `""` means "no class", not "any class"),
- `capacity.storage` >= the requested size (the user always gets at least what they asked for, possibly more),
- the same `volumeMode` (unset counts as `Filesystem`),
- matching the PVC's `spec.selector` labels if the selector is set (the selector is on the PVC, matched against PV labels),
- matching `volumeAttributesClassName` between claim and PV.
Among candidates the controller picks the smallest PV that fits. If the PVC sets `spec.volumeName`,
or the PV's `claimRef` names the claim, that pre-bound PV is used even if it fails some matching criteria
such as node affinity; the control plane still validates the storage class, access modes and
requested size.

## 3. Static provisioning by hand
```yaml
apiVersion: v1
kind: PersistentVolume
metadata: {name: pv-manual-01}
spec:
  capacity: {storage: 50Gi}
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  csi:
    driver: ebs.csi.aws.com
    volumeHandle: vol-0123456789abcdef0   # the actual cloud disk ID — must pre-exist
```
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: pvc-manual-01}
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: manual
  resources: {requests: {storage: 50Gi}}
```
For a statically provisioned class like `manual`, you can create a StorageClass with
`provisioner: kubernetes.io/no-provisioner` (the setting the Kubernetes docs use for local volumes) so
that no dynamic provisioning is attempted. Pre-binding: set `volumeName` on the PVC (with `storageClassName: ""`
or the PV's class) and optionally `claimRef` on the PV to stop other claims taking it.

## 4. Why a PVC stays Pending despite a matching-looking PV
- A PV already bound or reserved through `claimRef` for a different PVC (including one in another
  namespace) is not available to yours; PVs are cluster-scoped, PVCs namespaced.
- `volumeBindingMode: WaitForFirstConsumer` on the StorageClass: the PVC intentionally
  sits `Pending` with no PV until a pod referencing it is scheduled — this is normal,
  not broken. Check for a pod first before assuming provisioning failed.
- Quota is a different failure: a `ResourceQuota` (`requests.storage`, or the StorageClass-scoped key
  `<class>.storageclass.storage.k8s.io/requests.storage`) makes the API server reject the PVC
  creation with `403 Forbidden` and a message naming the constraint, so no Pending PVC appears.

## Gotchas
- With `Delete`, deleting the PVC deletes the PV and the underlying storage asset. For dynamically
  provisioned PVs the default reclaim policy is `Delete`; use `Retain` for anything irreplaceable (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.statefulsets-and-persistent-storage`).
- You can change the reclaim policy of an existing PV (the docs' task: `kubectl patch pv <name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'`) before deleting a PVC you might need back.

## Verify
- [ ] Explained, for a given PV, exactly which phase it's in and why.
- [ ] Hand-created a PV + PVC pair for a pre-existing disk and mounted it in a pod.
- [ ] Recovered a `Released` PV back to `Available` and rebound it.
- [ ] Diagnosed a `Pending` PVC down to quota, `WaitForFirstConsumer`, or a namespace
      mismatch — not just "provisioning is broken."

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed in the PV docs: phases, Retain/Released behaviour, pre-binding with volumeName/claimRef, no-provisioner, default Delete for dynamic PVs, reclaim-policy change task, 403 on quota violation. Confirmed in the pv_helpers.go FindMatchingVolume source: Available only, class, volumeMode, selector, capacity >= request, smallest match wins, pre-bound volume returned first. Corrected: a volumeName/claimRef pre-bound PV is not a total bypass (class, access modes and size are still validated), and quota violations reject the PVC with 403 rather than leaving it Pending. Removed the unconfirmed 'ties broken by name' and PV spec.csi immutability claims.

Method: documentation only; no commands were run.
