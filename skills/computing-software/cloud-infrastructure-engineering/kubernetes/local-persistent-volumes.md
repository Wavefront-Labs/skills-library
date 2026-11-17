---
id: computing-software.cloud-infrastructure-engineering.kubernetes.local-persistent-volumes
name: local-persistent-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-persistent-volume, local-pv, node-affinity, local-path-provisioner, local-static-provisioner, nvme, ssd, hostpath, kafka, cassandra, direct-attached-storage, das]
level: advanced
status: docs-checked
description: "Local PersistentVolumes: node-affinity binding, static provisioning with local-static-provisioner, and why node loss means data loss."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#local", "https://kubernetes.io/docs/concepts/storage/storage-classes/#local", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner", "https://github.com/rancher/local-path-provisioner"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local persistent volumes — when the disk never leaves the node

**Goal:** use node-attached NVMe/SSD for throughput that network-attached storage
can't match, without pretending it has the durability of a networked disk.

## 1. What a local PV actually is
A `PersistentVolume` pointing at a path/block device **on one specific node**, pinned
there with `nodeAffinity` (not optional — this is how the scheduler knows it can only
place the pod on that node):
```yaml
apiVersion: v1
kind: PersistentVolume
metadata: {name: local-pv-node3-disk1}
spec:
  capacity: {storage: 1500Gi}
  volumeMode: Filesystem
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-nvme
  local: {path: /mnt/disks/ssd1}
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - {key: kubernetes.io/hostname, operator: In, values: [node-3]}
```
`storageClassName` here has **no provisioner behind it**: local volumes can only be statically
created PersistentVolumes. The docs' StorageClass example uses
`provisioner: kubernetes.io/no-provisioner` with `volumeBindingMode: WaitForFirstConsumer`; local PVs are
created out-of-band (by hand or by an external static provisioner) and matched to PVCs the normal
binding way.

## 2. In practice: `local-static-provisioner`
Hand-writing a PV per disk per node doesn't scale. The external static provisioner
(sig-storage-local-static-provisioner) manages the lifecycle of local volumes: it creates and
cleans up PersistentVolumes for volumes it discovers under configured discovery directories
(mount each filesystem volume under a discovery directory; for Block mode, create a symbolic link
in it) and cleans up disks when released. It does not support dynamic provisioning. The local
volume docs note that without it, a local PV needs manual cleanup and deletion by the user.

`local-path-provisioner` (Rancher) is a separate *dynamic* option: it creates `hostPath` or `local`
based persistent volumes on demand and cleans up the volume content on the node automatically.
Check its README for its node-selection behaviour before using it beyond development clusters.

## 3. Why volumeBindingMode should be WaitForFirstConsumer
The Kubernetes docs recommend a StorageClass with `volumeBindingMode: WaitForFirstConsumer` for local
volumes. Delaying binding ensures the PVC binding decision is evaluated together with the pod's other
node constraints (resource requirements, node selectors, pod affinity and anti-affinity), using the
PV's `nodeAffinity` (which is mandatory for local volumes) when choosing the node.
Using `nodeName` in the pod spec bypasses the scheduler and leaves the PVC pending; use a node selector on
`kubernetes.io/hostname` instead.

## 4. Node loss
`local` volumes are subject to the availability of the underlying node. If a node becomes unhealthy,
the local volume becomes inaccessible and the pod using it cannot run. Applications must tolerate this
reduced availability, as well as potential data loss depending on the durability of the underlying
disk. Use local PVs when the application replicates its data across nodes; do not treat a single local
disk as durable.

## Gotchas
- `persistentVolumeReclaimPolicy: Delete` on a hand-made local PV is not accompanied by any cleanup
  of the files by itself; the docs say the PV needs manual cleanup and deletion unless the external
  static provisioner manages its lifecycle.
- A PV's `volumeMode` can be `Block` to expose the local volume as a raw block device.
- Local volume support for volume expansion is not documented; check before promising it.

## Verify
- [ ] Explained why `volumeBindingMode: WaitForFirstConsumer` is recommended for local PVs.
- [ ] Named how the application replicates data so that losing one node's disk is survivable.
- [ ] Confirmed cleanup behavior (manual or `local-static-provisioner`) before reusing
      a local PV's path for a new claim.
- [ ] Checked whether volume expansion is possible for this storage before promising it to a team.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: local volume statically created only, mandatory nodeAffinity, example PV shape, WaitForFirstConsumer recommendation and the nodeName caveat, no-provisioner example, Block volumeMode, node-availability caveat, manual cleanup note, external static provisioner behaviour (discovery directories, cleanup, no dynamic provisioning) and local-path-provisioner behaviour (dynamic, automatic cleanup). Removed unconfirmed claims: hostPath capacity/access-mode comparison, first-fit scheduling, cleanup-job wording, kubectl drain behaviour, 'expansion is not supported' (now stated as not documented), and the 'Immediate is rejected' claim.

Method: documentation only; no commands were run.
