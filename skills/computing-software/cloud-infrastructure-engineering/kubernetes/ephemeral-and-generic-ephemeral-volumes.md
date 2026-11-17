---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ephemeral-and-generic-ephemeral-volumes
name: ephemeral-and-generic-ephemeral-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, emptydir, generic-ephemeral-volume, csi-ephemeral-volume, tmpfs, sizelimit, scratch-space, pod-lifecycle, ephemeral-storage, projected-volume]
level: practitioner
status: docs-checked
description: "emptyDir medium/sizeLimit, generic ephemeral volumes backed by CSI with PVC-like features, and when scratch space should not be a PVC at all."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#emptydir", "https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/", "https://kubernetes.io/docs/concepts/storage/ephemeral-storage/", "https://kubernetes.io/docs/concepts/storage/volumes/#csi-ephemeral-volumes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral volumes — scratch space that doesn't need a PVC lifecycle

**Goal:** pick the right ephemeral storage mechanism for throwaway data, and know
which one actually needs StorageClass-grade features (snapshots, expansion) and which
doesn't.

## 1. `emptyDir` — simplest, node-local, gone with the pod
```yaml
volumes:
- name: scratch
  emptyDir:
    sizeLimit: 2Gi        # limits the volume's capacity; allocated from node ephemeral storage
    medium: Memory         # tmpfs — fast, but counts against the node's RAM, not disk
```
- Default medium is whatever backs the node (disk, SSD or network storage, depending on your
  environment). The storage is allocated from node ephemeral storage, and the kubelet counts
  `emptyDir` volumes (except tmpfs) toward a pod's local ephemeral-storage usage; if a pod uses
  more than you allow, the kubelet sets an eviction signal that triggers pod eviction. Set
  `sizeLimit` and ephemeral-storage requests/limits for production pods. If node ephemeral storage
  fills from other sources (logs, image overlays), the `emptyDir` may run out before its limit.
- `medium: Memory` mounts a tmpfs (RAM-backed filesystem): very fast, but files you write
  count against the memory limit of the container that wrote them. With no `sizeLimit`, memory-backed
  volumes are sized to node allocatable memory. Size it like a memory request, not a disk request.
- Data survives container crashes (a crash does not remove the pod from the node) but is
  deleted when the pod is removed from the node, so it does not survive a reschedule.

## 2. Generic ephemeral volumes — PVC features, pod-scoped lifecycle
```yaml
volumes:
- name: scratch-fast
  ephemeral:
    volumeClaimTemplate:
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: fast-ssd
        resources: {requests: {storage: 20Gi}}
```
This creates a real PVC (named `<pod>-<volume-name>`, a pod name and volume name joined by a hyphen) through the normal dynamic
provisioning path, but ties its lifecycle to the **pod**: when the pod is deleted, the PVC is
deleted too, and the volume goes with it because the default StorageClass reclaim policy is
Delete (a `Retain` class gives quasi-ephemeral storage that outlives the pod and needs separate
cleanup). It can be provided by any storage driver that supports persistent volumes, and the PVC can be a data source for
cloning or snapshots. It is **not** for anything you want to survive the pod. Because pod and volume names
determine the PVC name, avoid pod/volume name combinations that collide with other PVCs in the namespace.

## 3. CSI ephemeral volumes (inline, driver-managed)
A third mechanism: a `csi:` inline volume source directly in the pod spec (stable since
Kubernetes 1.25), for CSI drivers that specifically support it. Such volumes are ephemeral and
do not persist across pod restarts. Do not confuse it with generic ephemeral volumes above,
which work with any driver that also supports persistent volumes.

## 4. Choosing
- Pure scratch, small, node-local is fine, don't care about disk type: `emptyDir`
  with `sizeLimit`.
- Need a specific StorageClass's properties for scratch space: a generic ephemeral volume
  using that StorageClass.
- Need the data to survive pod deletion at all: neither — use a normal PVC
  (StatefulSet `volumeClaimTemplates` or a standalone PVC), not an ephemeral volume.

## Gotchas
- Generic ephemeral volumes let anyone who can create pods create PVCs indirectly; cluster
  administrators who do not want that can use an admission webhook to reject pods that use them.
  The normal namespace quota for PVCs still applies, so large or numerous ephemeral volumes count
  against `ResourceQuota`.
- Deleting the pod deletes the generic ephemeral PVC; a container restart alone does not.

## Verify
- [ ] Every `emptyDir` in a production manifest has a considered `sizeLimit` (and pods set ephemeral-storage requests/limits).
- [ ] Named why a specific ephemeral volume choice doesn't need PVC/snapshot features
      — if it does, it isn't actually ephemeral data.
- [ ] Confirmed a generic ephemeral volume's PVC and disk are cleaned up after pod
      deletion (`kubectl get pvc` shows nothing left behind).

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: emptyDir medium and sizeLimit behaviour, tmpfs counting against the writing container's memory limit, memory-backed default sizing, data surviving container crashes, generic ephemeral PVC naming/lifecycle/reclaim behaviour/quota/security note, and CSI inline volumes stable since v1.25. Removed unconfirmed claims: the node path `/var/lib/kubelet`, 'unlimited by default', Secrets Store as an example, `volumeMode: Block` for ephemeral claims and 'kubelet evicts the pod on sizeLimit' (the docs tie eviction to ephemeral-storage limits).

Method: documentation only; no commands were run.
