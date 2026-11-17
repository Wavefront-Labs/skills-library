---
id: computing-software.cloud-infrastructure-engineering.kubernetes.storage-capacity-aware-scheduling
name: storage-capacity-aware-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csistoragecapacity, storage-capacity-tracking, scheduler, waitforfirstconsumer, local-pv, topology, failedscheduling, capacity-exhausted]
level: advanced
status: docs-checked
description: "CSIStorageCapacity objects: how the scheduler avoids placing a pod on a node whose local/topology-constrained storage has no room left."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-capacity/", "https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1472-storage-capacity-tracking", "https://github.com/kubernetes/kubernetes/blob/master/pkg/scheduler/framework/plugins/volumebinding/binder.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage capacity-aware scheduling — stopping Pending before it happens

**Goal:** understand why some pods get `FailedScheduling` for storage reasons
*before* a PVC ever goes `Pending`, and when this feature matters at all.

## 1. The problem it solves
Without storage capacity tracking, the scheduler may choose a node that doesn't have enough
capacity to provision a volume, and multiple scheduling retries are needed. With tracking, the
scheduler only considers nodes that have enough storage available to them for the pod's missing volumes.
It applies when a pod uses a volume that has not been created yet, the volume's StorageClass
references a CSI driver and uses `WaitForFirstConsumer`, and the driver's `CSIDriver` object has
`storageCapacity: true`. With `Immediate` binding the driver picks where to create the volume,
independently of pods. CSI ephemeral volumes are always scheduled without considering capacity.

## 2. `CSIStorageCapacity`
A CSI driver that supports capacity tracking publishes `CSIStorageCapacity` objects in the namespace
where the driver is installed; each object holds capacity information for one StorageClass and defines
which nodes have access to that storage:
```bash
kubectl get csistoragecapacity -n <csi-namespace>
```
```yaml
apiVersion: storage.k8s.io/v1
kind: CSIStorageCapacity
metadata: {name: example, namespace: <csi-namespace>}
nodeTopology: {matchLabels: {topology.kubernetes.io/zone: us-east-1a}}
storageClassName: local-nvme
capacity: 400Gi
```
The check is simplistic: it only compares the size of the volume against the capacity listed in
`CSIStorageCapacity` objects whose topology includes the node. A node that fails it is
reported with the scheduler message `node(s) did not have enough free storage`.

## 3. When this matters
Storage whose capacity is finite per node or topology segment (for example local volumes served by a
CSI driver that supports capacity tracking; see
`computing-software.cloud-infrastructure-engineering.kubernetes.local-persistent-volumes`). Kubernetes
only provides the cluster-level API support: you must use a CSI driver that supports capacity tracking,
so consult the driver's documentation instead of assuming it is implemented.

## 4. Reading a capacity-related scheduling failure correctly
```bash
kubectl describe pod <pod>
# Events: FailedScheduling  ... node(s) did not have enough free storage.
kubectl get csistoragecapacity -n <csi-namespace> -o wide
```
Compare the requested PVC size against the `capacity` field of the CSIStorageCapacity objects whose
storage class and node topology match. Fix by adding capacity or shrinking the request.

## Gotchas
- Capacity tracking increases the chance that scheduling works on the first try but cannot guarantee it,
  because the scheduler decides on potentially out-of-date information. If the volume cannot really be
  created on the chosen node, the node selection is reset and the scheduler tries again.
- A pod with several volumes can fail permanently: one volume may already have been created in a
  topology segment that has no capacity left for another one. Manual intervention is needed (add
  capacity or delete the volume already created).
- It only works for drivers whose `CSIDriver` object sets `storageCapacity: true`.

## Verify
- [ ] Checked whether the CSI driver in use publishes `CSIStorageCapacity` before
      relying on pre-scheduling capacity filtering.
- [ ] Traced a `did not have enough free storage` scheduling event to the matching CSIStorageCapacity objects.
- [ ] Knows the check is based on possibly out-of-date information and can still need a retry.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed in the Storage Capacity concepts page: CSIStorageCapacity objects in the driver's namespace, CSIDriver.storageCapacity, the three scheduling conditions, the simplistic size comparison, rescheduling and the multi-volume limitation. Confirmed in binder.go: the scheduler reason is `node(s) did not have enough free storage` (the skill had `didn't have`). Removed unconfirmed claims about GET_CAPACITY, which drivers implement tracking, and a publish-interval cause.

Method: documentation only; no commands were run.
