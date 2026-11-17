---
id: computing-software.cloud-infrastructure-engineering.kubernetes.limitrange-pvc-size-bounds
name: limitrange-pvc-size-bounds
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, limitrange, limitrange-pvc, storage-quota, persistentvolumeclaim]
level: practitioner
status: docs-checked
description: "Bound PersistentVolumeClaim sizes per namespace with a LimitRange of type PersistentVolumeClaim, combined with storage quotas per StorageClass."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/limit-storage-consumption/", "https://kubernetes.io/docs/concepts/policy/limit-range/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#storage-resource-quota"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LimitRange for PVC sizes

## Min and max per claim
```yaml
apiVersion: v1
kind: LimitRange
metadata: {name: storage-bounds, namespace: team-a}
spec:
  limits:
  - type: PersistentVolumeClaim
    min: {storage: 1Gi}
    max: {storage: 100Gi}
```
A PVC outside the range is rejected at admission:
```
persistentvolumeclaims "data" is forbidden: maximum storage usage per PersistentVolumeClaim is 100Gi, but request is 500Gi
```
The LimitRange admission controller applies to create and update requests: an object that violates a
constraint is rejected with `403 Forbidden` and a message naming the constraint.

## Pair with quota for totals
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: storage, namespace: team-a}
spec:
  hard:
    requests.storage: 500Gi
    persistentvolumeclaims: "20"
    fast-ssd.storageclass.storage.k8s.io/requests.storage: 100Gi
    fast-ssd.storageclass.storage.k8s.io/persistentvolumeclaims: "5"
```
LimitRange caps a single claim; quota caps the sum and the count, optionally per StorageClass.

## Why min matters
Minimum storage requests are used when the underlying storage provider requires certain minimums; the
Kubernetes task page gives AWS EBS volumes' 1Gi minimum as the example.

## Verify
```bash
kubectl describe limitrange storage-bounds -n team-a
kubectl apply -n team-a --dry-run=server -f big-pvc.yaml     # expect 403 forbidden
```

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: LimitRange type PersistentVolumeClaim with min/max storage, rejection at admission (403, create or update), ResourceQuota keys requests.storage, persistentvolumeclaims and the per-class <class>.storageclass.storage.k8s.io/requests.storage and /persistentvolumeclaims, and the error wording in the limitranger admission source. Removed the unconfirmed gp2/pd-standard IOPS and CSI minimum-size claims.

Method: documentation only; no commands were run.
