---
id: computing-software.cloud-infrastructure-engineering.kubernetes.change-pv-reclaim-policy-and-reuse-retained-pvs
name: change-pv-reclaim-policy-and-reuse-retained-pvs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, patch-reclaim-policy, reclaim-policy, persistentvolume, retain, claimref, cka, storage]
level: practitioner
status: docs-checked
description: "Switch existing PVs from Delete to Retain before risky changes, then rebind a Released PV to a new PVC by clearing or pre-setting claimRef."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#reclaiming", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#reserving-a-persistentvolume"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing reclaim policy on existing PVs

## Why
Dynamically provisioned PVs inherit the StorageClass `reclaimPolicy` (default `Delete`), so deleting the PVC deletes the PV and the storage asset. Switch critical PVs to `Retain` first.

## Change it
```bash
kubectl get pv
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
kubectl get pv -o custom-columns=PV:.metadata.name,CLAIM:.spec.claimRef.name,NS:.spec.claimRef.namespace,POLICY:.spec.persistentVolumeReclaimPolicy
```
A StorageClass `reclaimPolicy` applies only to PVs provisioned afterwards (valid values `Delete` or `Retain`); create a separate class with `Retain` for future volumes.

## Reuse a Released PV
With `Retain`, deleting the PVC leaves the PV `Released` and not available to other claims because the previous claimant's data remains. Documented manual reclamation: delete the PV, clean up the data on the storage asset, delete the asset; or, to reuse the same asset, create a new PV pointing at it. To rebind an existing PV instead:
```bash
# free it for any matching claim: remove the claimRef
kubectl patch pv <pv-name> --type json -p '[{"op":"remove","path":"/spec/claimRef"}]'
```
Then pre-bind with the claim (empty `storageClassName` must be set explicitly or the default class is applied):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: foo-pvc, namespace: foo}
spec:
  storageClassName: ""
  volumeName: foo-pv
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 10Gi}}
```
`volumeName` alone does not stop other claims from taking the PV; reserve it by setting `spec.claimRef` (name and namespace of the PVC) on the PV. Binding happens regardless of node affinity, but the storage class, access modes and size must still be valid.

## Deletion protection finalizer
The `HonorPVReclaimPolicy` feature (beta and on by default from 1.31, stable in 1.33) adds the finalizer `external-provisioner.volume.kubernetes.io/finalizer` so that PVs with `Delete` policy are removed only after the backing storage is deleted.

## Return to Delete
Switch back to `Delete` once the data is no longer needed; otherwise storage assets keep existing. List `Released` PVs regularly (STATUS column of `kubectl get pv`).

## Verify
- [ ] `kubectl get pv <pv-name>` shows `Retain` before destructive operations.
- [ ] After rebinding, the PVC is `Bound` to the intended PV.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: reclaim policy semantics, claimRef and volumeName reservation, HonorPVReclaimPolicy stages and finalizer.

Method: documentation only; no commands were run.
