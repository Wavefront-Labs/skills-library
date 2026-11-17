---
id: computing-software.cloud-infrastructure-engineering.kubernetes.delete-reclaim-policy-data-loss
name: delete-reclaim-policy-data-loss
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, access-modes-reclaim, delete-reclaim-policy, persistentvolume, data-protection, retain]
level: practitioner
status: docs-checked
description: "Prevent data loss from the default Delete reclaim policy when PVCs, namespaces or Helm releases are removed, by switching critical PVs to Retain and adding guardrails."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#reclaiming", "https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#persistentvolumeclaim-retention"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delete reclaim policy risks

Dynamically provisioned PVs inherit the StorageClass `reclaimPolicy`, which defaults to `Delete`. With `Delete`, removing the PVC removes both the PV object and the storage asset in the external infrastructure (for volume plugins that support it).

Things that remove PVCs and therefore data under `Delete`:
- Deleting the PVC, or anything that owns or templates it. For StatefulSets, `.spec.persistentVolumeClaimRetentionPolicy` (feature `StatefulSetAutoDeletePVC`, stable in 1.32) with `whenDeleted: Delete` or `whenScaled: Delete` deletes PVCs; the default for both is `Retain`.
- Tools that prune or uninstall resources they manage. Helm skips deleting a resource annotated `helm.sh/resource-policy: keep` on uninstall, upgrade or rollback, but the resource is then orphaned and no longer managed by Helm.

## Protect critical data
```bash
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
kubectl get pv -o custom-columns=PV:.metadata.name,CLAIM:.spec.claimRef.name,NS:.spec.claimRef.namespace,POLICY:.spec.persistentVolumeReclaimPolicy
```
- Use a separate StorageClass with `reclaimPolicy: Retain` for databases (the class setting applies to PVs created after the class is used).
- Take VolumeSnapshots on a schedule independent of the PV lifecycle (see `volume-snapshot-scheduling-consistency-and-cross-namespace-restore`).
- Set the StatefulSet retention policy to `Retain` (the default) unless you want automatic cleanup.

## With Retain
Deleting the PVC leaves the PV `Released` with the data intact. Rebind by removing the PV's `claimRef` and creating a PVC with `volumeName` (see `change-pv-reclaim-policy-and-reuse-retained-pvs`), or delete the PV and the storage asset deliberately.

## Verify
In a test namespace, delete a PVC bound to a `Retain` PV: the PV goes `Released` and the storage asset still exists.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: Delete default and behaviour, StatefulSet PVC retention policy, Helm resource-policy keep annotation.

Method: documentation only; no commands were run.
