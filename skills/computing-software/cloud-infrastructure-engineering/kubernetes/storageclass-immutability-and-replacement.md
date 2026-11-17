---
id: computing-software.cloud-infrastructure-engineering.kubernetes.storageclass-immutability-and-replacement
name: storageclass-immutability-and-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storageclass, storageclass-immutable, dynamic-provisioning, storage-migration]
level: practitioner
status: docs-checked
description: "Change a StorageClass whose parameters are immutable by deleting and recreating it, knowing what happens to existing PVs, PVCs and the default class."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-classes/", "https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/storage/v1/types.go", "https://github.com/kubernetes/kubernetes/blob/master/pkg/apis/storage/validation/validation.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StorageClass immutability

`provisioner`, `parameters`, `reclaimPolicy` and `volumeBindingMode` cannot be changed after
creation:
```
The StorageClass "fast" is invalid: parameters: Forbidden: updates to parameters are forbidden.
```
Labels, annotations (including the default-class annotation), `mountOptions`, `allowVolumeExpansion` and
`allowedTopologies` are not marked immutable in the `storage.k8s.io/v1` API and can be updated in place.

## Replace a class
```bash
kubectl get sc fast -o yaml > fast-old.yaml
# edit parameters, strip metadata.uid/resourceVersion/creationTimestamp
kubectl delete sc fast
kubectl apply -f fast-new.yaml
```
- Existing PVs keep the settings they were created with.
- Existing PVCs reference the class by name; PVCs created while the class is missing cannot use it, so do the swap
  in a quiet window.
- Expansion of a PVC depends on its class having `allowVolumeExpansion: true`.

## Prefer a new name for meaningful changes
Create `fast-v2`, point new workloads at it, migrate data if needed, keep `fast` until no PVC uses it:
```bash
kubectl get pvc -A -o jsonpath='{range .items[?(@.spec.storageClassName=="fast")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'
```
For performance changes on existing volumes, use VolumeAttributesClass where the driver supports it.

## Verify
`kubectl get sc` shows the new class (and exactly one default); a test PVC provisions with the new parameters.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed in the storage.k8s.io/v1 API types: provisioner, parameters, reclaimPolicy and volumeBindingMode are marked immutable; mountOptions, allowVolumeExpansion and allowedTopologies are not. Confirmed in the validation source that the update error reads 'parameters: Forbidden: updates to parameters are forbidden.'. Removed the GitOps tool claims, which no checked source covers, and the exact 'not found' message.

Method: documentation only; no commands were run.
