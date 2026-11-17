---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volume-expansion-internals
name: volume-expansion-internals
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-expansion, allowvolumeexpansion, filesystemresizepending, external-resizer, controllerexpandvolume, nodeexpandvolume, ext4, xfs, online-resize, offline-resize, pvc-resize]
level: advanced
status: docs-checked
description: "How PVC expansion actually runs: the two-step controller/node resize, the FileSystemResizePending condition, and why you cannot shrink a volume."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims", "https://kubernetes-csi.github.io/docs/volume-expansion.html", "https://kubernetes-csi.github.io/docs/external-resizer.html", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/core/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume expansion internals — what actually happens when you bump storage size

**Goal:** know the two separate resize steps, read `FileSystemResizePending`
correctly, and stop assuming a bigger number in the YAML means a bigger disk
immediately.

## 1. Two resize calls, not one
Expansion is an edit to the **PVC**, never the PV or the StorageClass:
```bash
kubectl patch pvc db-data-db-0 -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'
```
You can only expand a PVC if its StorageClass has `allowVolumeExpansion: true`, and for CSI volumes the
driver must support expansion. Editing the PVC resizes the existing volume; a new PV is never created.
Two CSI calls follow:
1. **`ControllerExpandVolume`** — driven by the `external-resizer` sidecar; the CSI spec lets a driver
   declare whether this can happen while the volume is online (published on a node) or offline.
2. **`NodeExpandVolume`** — kubelet, via the node plugin; it always requires the volume to be published
   or staged on a node, and is typically used to expand the file system on the node.

Between steps, the PVC shows condition `FileSystemResizePending` ("controller resize is finished and a file
system resize is pending on node" in the API type) — this is not an error. For a volume with a file system,
the file system is only resized when a pod is using the PVC in `ReadWrite` mode: when the pod starts, or
while it runs if the file system supports online expansion.
```bash
kubectl get pvc db-data-db-0 -o jsonpath='{.status.conditions}'
```

## 2. Online vs. requires-restart
In-use PVCs can be expanded without recreating the pod or deployment (stable since Kubernetes 1.24): the
PVC becomes available to its pod once its file system has been expanded. Whether a given driver does this
online depends on its capabilities: check its documentation. If a PVC sits at `FileSystemResizePending`,
check that a pod is using it in ReadWrite mode and look at the resizer and node plugin logs.

## 3. Filesystem and volume-mode differences
- You can only resize volumes containing a file system if it is XFS, Ext3 or Ext4.
- Raw block volumes (`volumeMode: Block`): there is no file system to grow; the application sees the
  larger device (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.raw-block-volumes`).

## 4. Shrinking
Kubernetes does not support shrinking a PVC to less than its current size. The practical path is to
provision a new, smaller PVC, copy the data at the application layer, cut over, and delete the old PVC.

## 5. Failed expansion and StatefulSets
If expansion fails (for example the requested size is too big for the backend), it is retried continuously.
Documented recovery: retry with a smaller size that is still higher than `.status.capacity` (monitor
`.status.allocatedResourceStatuses` and events), or, as an administrator, use the Retain-and-recreate
procedure in the PV docs. For StatefulSets, see
`computing-software.cloud-infrastructure-engineering.kubernetes.pvc-expansion-failure-recovery-and-statefulset-volumes`.

## Gotchas
- Editing the capacity of a PersistentVolume directly and then making the PVC match it prevents an
  automatic resize: the control plane concludes the backing volume was already enlarged by hand.
- `kubectl get pvc` shows the requested size in `spec`; compare with `status.capacity` for the actual size.

## Verify
- [ ] Resized a PVC and confirmed the file system actually grew (`df -h` inside the pod), not just the API object.
- [ ] Explained the difference between `ControllerExpandVolume` and
      `NodeExpandVolume` and which condition tracks which.
- [ ] Named the shrink workaround (new PVC + app-level copy) rather than looking for a
      shrink API that doesn't exist.
- [ ] Checked the CSI driver's documentation for online expansion support before promising it.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: allowVolumeExpansion requirement, in-use expansion stable since 1.24, XFS/Ext3/Ext4 only, file system resized when a pod uses the PVC in ReadWrite mode, shrinking unsupported, failure-recovery methods, the direct-PV-edit warning, ControllerExpandVolume online/offline and NodeExpandVolume semantics (CSI docs), FileSystemResizePending condition meaning (core/v1 types). Removed unconfirmed claims: cloud block types are all online, resize2fs/xfs_growfs behaviour, 'API rejects patch with no field set' wording, driver size rounding, and the claim that volumeClaimTemplates edits only affect new ordinals.

Method: documentation only; no commands were run.
