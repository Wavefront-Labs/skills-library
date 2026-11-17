---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pvc-expansion-failure-recovery-and-statefulset-volumes
name: pvc-expansion-failure-recovery-and-statefulset-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-expansion, expansion-failure-recovery, recovervolumeexpansionfailure, statefulset-pvc-expansion, volumeclaimtemplates, persistentvolumeclaim]
level: advanced
status: docs-checked
description: "Recover from a failed PVC expansion (request too large, quota, provider limits) and expand StatefulSet volumes despite immutable volumeClaimTemplates via orphan-and-recreate."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#recovering-from-failure-when-expanding-volumes", "https://kubernetes.io/blog/2025/09/19/kubernetes-v1-34-recover-expansion-failure/", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#volume-claim-templates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PVC expansion: failure recovery and StatefulSet volumes

## When expansion fails
If the new size is too big for the storage system, the expansion is retried continuously until someone acts. Expansion needs a StorageClass with `allowVolumeExpansion: true` and a CSI driver that supports it; filesystems can be resized only if they are XFS, Ext3 or Ext4, and the filesystem is resized when a Pod uses the PVC in read/write mode (at Pod start, or online if the filesystem supports it).
```bash
kubectl describe pvc data-db-0
kubectl get pvc data-db-0 -o jsonpath='{.status.allocatedResourceStatuses}{"\n"}{.status.capacity}'
```
Progress states for block volumes are `ControllerResizeInProgress`, `NodeResizePending`, `NodeResizeInProgress`; infeasible sizes show `ControllerResizeInfeasible` or `NodeResizeInfeasible`. Errors are also recorded as PVC conditions `ControllerResizeError` or `NodeResizeError`. A PVC with the `FileSystemResizePending` condition has finished the controller resize and waits for the filesystem resize on the node.

### Recovery by requesting a smaller size
`RecoverVolumeExpansionFailure` was beta (on by default) in 1.32 and stable in 1.34. Edit the PVC request to a value smaller than the failed one but still greater than `.status.capacity`; Kubernetes never shrinks below the size already allocated. Quota consumed by the failed expansion is returned.
```bash
kubectl patch pvc data-db-0 -p '{"spec":{"resources":{"requests":{"storage":"150Gi"}}}}'
```

### Manual recovery (cluster admin)
1. Set the bound PV's reclaim policy to `Retain`.
2. Delete the PVC (data is kept because of Retain).
3. Remove the `claimRef` from the PV so it becomes `Available`.
4. Recreate the PVC with a size smaller than the PV and `volumeName` set to the PV.
5. Restore the PV's original reclaim policy.

## Expanding StatefulSet volumes
`volumeClaimTemplates` cannot be updated on an existing StatefulSet (the API server treats the field as immutable), while the PVCs created from it are ordinary PVCs.
1. Patch each existing PVC:
```bash
for i in 0 1 2; do kubectl patch pvc data-db-$i -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'; done
kubectl get pvc -w
```
2. To make new replicas use the new size, delete the StatefulSet object without deleting Pods (`--cascade=orphan`) and re-apply it with the larger template:
```bash
kubectl get sts db -o yaml > db.yaml      # edit volumeClaimTemplates storage; remove status, uid, resourceVersion
kubectl delete sts db --cascade=orphan
kubectl apply -f db.yaml
```
`--cascade=orphan` leaves the Pods running; the recreated StatefulSet adopts them.

## Gotchas
- Editing a PV's capacity by hand and then matching the PVC to it prevents the real resize from happening.
- Expansion is one-way; alert on free space (the kubelet exposes `kubelet_volume_stats_available_bytes` and `kubelet_volume_stats_capacity_bytes`, alpha-stability metrics labelled by namespace and persistentvolumeclaim).

## Verify
- [ ] All PVCs report the new capacity and the filesystem inside the Pods matches.
- [ ] The StatefulSet template shows the new size.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: RecoverVolumeExpansionFailure stages (beta 1.32, stable 1.34), the lower-size rule, resize states and conditions, filesystem resize rules, volumeClaimTemplates immutability in the API validation source.

Method: documentation only; no commands were run.
