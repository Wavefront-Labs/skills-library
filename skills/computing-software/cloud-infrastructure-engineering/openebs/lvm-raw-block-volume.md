---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-raw-block-volume
name: lvm-raw-block-volume
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, raw-block, volumemode-block, volumedevices, storageclass, databases]
level: practitioner
status: docs-checked
description: "Provision a raw block volume on Local PV LVM: StorageClass without fstype, PVC with volumeMode Block, volumeDevices in the pod, and why mountOptions are not applied."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-raw-block-volume
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-resize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some applications, most commonly databases, want direct access to a block device because the filesystem layer adds overhead they do not need. Local PV LVM can attach a raw block device to the pod.

Steps from the guide:

1. **StorageClass.** Create it **without an `fstype`**, since a raw block volume has no filesystem type. Because the volume is attached as a block device rather than mounted, the `mountOptions` and `formatOptions` in the class are not used.
2. **PVC.** Request the volume with `volumeMode: Block`.
3. **Pod.** Reference the PVC under `volumeDevices` (not `volumeMounts`) and give the device path. The driver attaches the raw device at that path; in the guide's example the application sees it at `/dev/xvda` inside the pod.

The page notes that running database software and storage infrastructure software inside Kubernetes makes raw block support increasingly important. Related behaviour from the resize guide: online expansion for `Block` mode requires Kubernetes 1.23 or later. The page's example class sets `allowVolumeExpansion: true` and a `volgroup` parameter with the `local.csi.openebs.io` provisioner; the PVC is ReadWriteOnce with `volumeMode: Block` and `storage: 5Gi`.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-raw-block-volume) in full, plus the lvm-resize page for the Kubernetes 1.23 note. Claims match the pages. Removed the unsourced advice to copy manifests rather than assemble them; the "not volumeMounts" contrast is inferred from the example, which only uses volumeDevices.
