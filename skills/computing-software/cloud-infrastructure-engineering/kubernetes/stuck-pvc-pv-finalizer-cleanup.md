---
id: computing-software.cloud-infrastructure-engineering.kubernetes.stuck-pvc-pv-finalizer-cleanup
name: stuck-pvc-pv-finalizer-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, finalizer, pvc-protection, pv-protection, stuck-terminating, kubectl-patch, volumeattachment, force-cleanup, namespace-stuck-terminating]
level: advanced
status: docs-checked
description: "Why a PVC or PV sticks in Terminating forever, what pvc-protection/pv-protection finalizers are actually guarding against, and the safe cleanup order."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storage-object-in-use-protection", "https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/", "https://kubernetes.io/docs/concepts/storage/volume-snapshots/#persistent-volume-claim-as-snapshot-source-protection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stuck Terminating PVCs and PVs — reading finalizers before removing them

**Goal:** know what `kubernetes.io/pvc-protection` and `kubernetes.io/pv-protection`
are actually preventing, so clearing them doesn't trade a stuck object for data loss
or an orphaned cloud disk.

## 1. What's actually stuck, and why
`kubectl delete pvc` (or `pv`) sets `deletionTimestamp` and the object enters
`Terminating` — but it is **not removed** from etcd until every finalizer on it is
cleared. Two built-in ones matter here:
- `kubernetes.io/pvc-protection` — protects a PVC that is in active use by a pod (a pod object
  exists that uses it): removal is postponed until no pod uses it. The same protection applies while a
  snapshot is being taken from the PVC. It exists so deleting a PVC in use doesn't remove the volume
  out from under the pod, which could cause data loss.
- `kubernetes.io/pv-protection` — stays on a PV as long as it's still `Bound` to a PVC.
Check which is actually present and why, first:
```bash
kubectl get pvc <name> -o jsonpath='{.metadata.finalizers}'
kubectl describe pvc <name>        # status Terminating and Finalizers list
```

## 2. The right fix is almost always upstream, not the finalizer
If `pvc-protection` is blocking because a pod still references the PVC: delete (or
let finish terminating) the pod first — that's the finalizer doing its job
correctly, not a bug. If the pod itself is stuck Terminating (common with a dead
node, see
`computing-software.cloud-infrastructure-engineering.kubernetes.multi-attach-and-stuck-volumeattachment`),
fix that first; the PVC will then clear on its own.

## 3. When it's genuinely stuck (not just waiting correctly)
Confirm with evidence before patching anything:
- `kubectl get pods -A` — is there a pod stuck Terminating or still using the PVC? Check whether its node
  is really gone (same precaution as the multi-attach skill).
- `kubectl get volumeattachment` — check for attachments that still reference the volume.
Only once the referencing pod and node situation is understood and genuinely
unrecoverable:
```bash
kubectl patch pvc <name> -p '{"metadata":{"finalizers":null}}' --type=merge
```
This removes the finalizer so the PVC object can be deleted. The Kubernetes finalizer documentation
warns against manually removing finalizers: do it only when the purpose of the finalizer is
understood and is accomplished in another way. With a PV `reclaimPolicy` of `Delete`, deleting the PVC
also deletes the PV and the underlying storage asset; if the disk might still be needed, change the PV's
reclaim policy to `Retain` first (`kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'`).

## 4. Namespace stuck Terminating because of a PVC
A namespace delete waits for the objects in it, so a PVC held by `pvc-protection` can hold up namespace
deletion. Fix the PVC and the pod using it first. Check for leftover PVs (cluster-scoped) afterwards:
`kubectl get pv` shows the CLAIM column.

## Gotchas
- Finalizers are added for a reason; removing one stops Kubernetes from doing what it protected. Do it
  once you understand the specific condition, not as a generic "stuck resource" fix.
- A PV with `Retain` whose PVC is deleted sits `Released` — see
  `computing-software.cloud-infrastructure-engineering.kubernetes.pv-pvc-binding-internals`
  to either reclaim or delete it.
- After a forced cleanup, check the storage backend that the disk's real state matches what Kubernetes now believes.

## Verify
- [ ] Identified the exact finalizer present and the specific condition it's waiting
      on, before patching anything.
- [ ] Resolved the upstream cause (pod still running, node not actually dead) first,
      and only used `finalizers: null` patching when genuinely unrecoverable.
- [ ] Checked `reclaimPolicy` and flipped to `Retain` first if disk-level data might
      still be needed.
- [ ] After a forced cleanup, verified no orphaned PV or backend disk/attachment was left behind.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: pvc-protection and pv-protection behaviour and the Terminating status with Finalizers shown by describe (PV docs), snapshot-source protection, finalizer deletion semantics and the documented warning against manually removing finalizers, and the reclaim-policy patch. Removed unconfirmed claims: `jq` filter, 'Used by Pods' output, namespace finalize trick via the raw API, and the claim that clearing a finalizer detaches nothing at cloud level.

Method: documentation only; no commands were run.
