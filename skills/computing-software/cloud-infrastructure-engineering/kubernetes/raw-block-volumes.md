---
id: computing-software.cloud-infrastructure-engineering.kubernetes.raw-block-volumes
name: raw-block-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volumemode, block, raw-block-volume, devicepath, blockdevices, databases, ceph-rbd, direct-io, filesystem-bypass]
level: advanced
status: docs-checked
description: "volumeMode: Block PersistentVolumes: raw device mounts with devicePath, which workloads benefit, and the filesystem features you lose."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#raw-block-volume-support", "https://kubernetes-csi.github.io/docs/raw-block.html", "https://kubernetes-csi.github.io/docs/volume-expansion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw block volumes — handing a pod the disk, not a filesystem

**Goal:** know when skipping the filesystem is worth it, and the operational cost of
doing so (no `df`, no `cp`, no fsck safety net).

## 1. The API surface
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: raw-pvc}
spec:
  accessModes: [ReadWriteOnce]
  volumeMode: Block            # default is Filesystem — must opt in explicitly
  storageClassName: fast-ssd
  resources: {requests: {storage: 100Gi}}
---
# in the pod spec
containers:
- name: app
  volumeDevices:               # NOT volumeMounts — different stanza entirely
  - {name: raw, devicePath: /dev/xvda}
volumes:
- {name: raw, persistentVolumeClaim: {claimName: raw-pvc}}
```
No `mountPath`, no `subPath`, no `mountPropagation` — none of the filesystem-mount
machinery applies. The container sees a block device node at `/dev/xvda` and is
responsible for everything above that: partitioning (usually skipped), formatting (if
it wants a filesystem at all), or direct I/O against the raw blocks.

## 2. Who wants this
Applications that must handle a raw block device themselves: the Kubernetes docs say the application
running in the pod must know how to handle a raw block device. Choose it for a storage engine built
to use one, not as a default performance knob.

Supported volume plugins (docs): CSI (including some CSI-migrated volume types), FC, iSCSI and local volumes.
CSI has no capability query for block volumes: Kubernetes passes requests to the driver, which may fail
with `InvalidArgument` if it does not support block, so check that the StorageClass's driver supports it.

## 3. What changes
- A container gets a device path (`volumeDevices.devicePath`) instead of a mount path, so there is
  no directory to inspect with `df` or write files into; the application manages everything above the device.
- Binding is strict about `volumeMode`: a Block PVC binds only to a Block PV, and an unspecified or
  Filesystem PVC never binds to a Block PV (see the binding matrix in the PV docs).
- Snapshots work through VolumeSnapshots; `sourceVolumeMode` records whether the snapshot's source was
  `Filesystem` or `Block`, and restoring with a different mode needs the
  `snapshot.storage.kubernetes.io/allow-volume-mode-change: "true"` annotation on the VolumeSnapshotContent.
  File-level backup tools cannot read inside a raw device; use snapshot-based paths.

## 4. Expansion
PVC expansion needs `allowVolumeExpansion: true` on the StorageClass and a driver that supports it.
The CSI docs describe `NodeExpandVolume` as typically used to expand the file system on the node;
for a block-mode volume, check your driver's documentation for what it does and whether the application
must detect the new size.

## Gotchas
- Two writers on one raw device is the application's problem to prevent; Kubernetes provides no
  file-level coordination. The common case is `ReadWriteOnce` with one writer.
- The PVC `volumeMode` is chosen at creation; if you need the other mode, create a new PVC and copy
  the data through the application.

## Verify
- [ ] Named a concrete reason (an application built to use a raw device) to use raw block.
- [ ] Confirmed the driver supports block volumes and what it does on expansion.
- [ ] Verified the backup path is snapshot-based, not file-level, for this volume.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: volumeMode Block, volumeDevices/devicePath manifest shape, the Block/Filesystem binding matrix, supported plugins list, CSI block behaviour, NodeExpandVolume description, sourceVolumeMode and the allow-volume-mode-change annotation. Removed all unsourced claims about which databases benefit, performance effects, fsGroup/SELinux behaviour, tooling gaps, and the claim that expansion needs no node step.

Method: documentation only; no commands were run.
