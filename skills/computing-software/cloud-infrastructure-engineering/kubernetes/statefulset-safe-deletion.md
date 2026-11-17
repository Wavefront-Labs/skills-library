---
id: computing-software.cloud-infrastructure-engineering.kubernetes.statefulset-safe-deletion
name: statefulset-safe-deletion
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, statefulset, statefulset-deletion, cascade-orphan, persistentvolumeclaimretentionpolicy]
level: practitioner
status: docs-checked
description: "Delete or recreate a StatefulSet safely: scale to zero for ordered termination, orphan pods to change immutable fields, and keep or delete PVCs on purpose."
sources: ["https://kubernetes.io/docs/tasks/run-application/delete-stateful-set/", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#persistentvolumeclaim-retention"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting a StatefulSet safely

## Ordered shutdown
StatefulSets give no guarantee on pod termination order when the StatefulSet is deleted. To get
ordered, graceful termination, scale to 0 first:
```bash
kubectl scale sts db --replicas=0
kubectl rollout status sts db          # or watch pods disappear highest ordinal first
kubectl delete sts db
```

## PVCs survive by default
`volumeClaimTemplates` PVCs are not deleted with the StatefulSet or on scale-down unless
`persistentVolumeClaimRetentionPolicy` says so (field stable since 1.32, default `Retain`):
```yaml
persistentVolumeClaimRetentionPolicy:
  whenDeleted: Retain     # or Delete
  whenScaled: Retain      # or Delete
```
To remove data deliberately afterwards:
```bash
kubectl delete pvc -l app=db       # PV reclaimPolicy decides if the disk is destroyed
```

## Recreate to change immutable fields (volumeClaimTemplates, selector, serviceName, podManagementPolicy)
```bash
kubectl get sts db -o yaml > db-backup.yaml
kubectl delete sts db --cascade=orphan      # pods keep running, now ownerless
# edit and apply the new StatefulSet with the SAME name and selector
kubectl apply -f db-new.yaml               # adopts the orphaned pods and existing PVCs
kubectl rollout restart sts db             # optional: roll pods onto the new template
```
Existing PVCs are matched by name (`<template>-<sts>-<ordinal>`); `volumeClaimTemplates` is immutable on an existing
StatefulSet, and the new template does not change or resize existing PVCs, so expand them separately.

## Gotchas
- The controller adopts orphaned pods whose labels match the new selector; if the selector does not match they stay orphaned.
- The headless Service is not deleted with the StatefulSet; delete it separately only when you are done with the peer DNS names.
- Back up data (snapshot) before any deletion in production.

## Verify
`kubectl get pods -l app=db -o jsonpath='{.items[*].metadata.ownerReferences[0].name}'` shows the
new StatefulSet owning the pods; PVCs remain Bound.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed: StatefulSets do not guarantee pod termination order on deletion and the docs advise scaling to 0 first (Limitations section); `persistentVolumeClaimRetentionPolicy` with `whenDeleted` and `whenScaled`, values Retain (default) or Delete, gate StatefulSetAutoDeletePVC stable in 1.32; `kubectl delete --cascade=orphan` leaves pods behind (delete-stateful-set task); PVCs are not deleted with pods and deleting a PVC may delete the PV depending on reclaim policy. Kubernetes source: StatefulSet update validation marks selector, volumeClaimTemplates, serviceName and podManagementPolicy immutable; the StatefulSet controller adopts matching orphan pods (ClaimPods); PVC names are `<claim>-<set>-<ordinal>`.
Removed: a "recreate the headless Service first" remark that no documentation states.

Method: documentation only; no commands were run.
