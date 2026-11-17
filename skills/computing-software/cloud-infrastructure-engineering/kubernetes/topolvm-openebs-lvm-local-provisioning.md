---
id: computing-software.cloud-infrastructure-engineering.kubernetes.topolvm-openebs-lvm-local-provisioning
name: topolvm-openebs-lvm-local-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-raw-block-volumes, topolvm, openebs-lvm, local-storage, csi]
level: practitioner
status: docs-checked
description: "Provision local NVMe or disk storage dynamically from per-node LVM volume groups with TopoLVM or OpenEBS LVM LocalPV, with capacity-aware scheduling."
sources: ["https://github.com/topolvm/topolvm/blob/main/docs/advanced-setup.md", "https://github.com/topolvm/topolvm/blob/main/docs/lvmd.md", "https://github.com/topolvm/topolvm/blob/main/charts/topolvm/README.md", "https://github.com/openebs/lvm-localpv/blob/develop/docs/storageclasses.md", "https://github.com/openebs/lvm-localpv/blob/develop/docs/quickstart.md", "https://kubernetes.io/docs/concepts/storage/storage-capacity/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic local provisioning with LVM

Static local PVs need a hand-made PV per disk. LVM-based CSI drivers carve logical volumes from a
volume group on each node on demand, with expansion and snapshots.

## Node preparation (each node)
```bash
pvcreate /dev/nvme1n1 /dev/nvme2n1
vgcreate myvg1 /dev/nvme1n1 /dev/nvme2n1
```

## TopoLVM
```yaml
# Helm values: map device classes to volume groups, and create the StorageClass
lvmd:
  deviceClasses:
  - {name: ssd, volume-group: myvg1, default: true, spare-gb: 10}
storageClasses:
- name: topolvm-provisioner
  storageClass:
    fsType: xfs                  # ext4, xfs or btrfs (beta)
    allowVolumeExpansion: true
    volumeBindingMode: WaitForFirstConsumer
    additionalParameters: {}     # extra StorageClass parameters, such as a device-class choice
```
The chart renders a StorageClass with provisioner `topolvm.io` and the `csi.storage.k8s.io/fstype`
parameter. For a non-default device class, set it through `additionalParameters` as described in the
TopoLVM advanced-setup document. `spare-gb` (default 10) is storage capacity kept spare per device
class. `WaitForFirstConsumer` is recommended because TopoLVM cannot schedule pods well with
`Immediate` binding. TopoLVM uses Kubernetes storage capacity tracking by default (chart value
`controller.storageCapacityTracking.enabled`) so the scheduler avoids nodes without room.

## OpenEBS LVM LocalPV
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: openebs-lvm}
provisioner: local.csi.openebs.io
parameters: {storage: lvm, volgroup: myvg1, fsType: ext4}
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```
`volgroup` names one volume group; `vgpattern` (a regular expression) can be used instead.
`fsType` supports ext2, ext3, ext4, xfs and btrfs and defaults to ext4. Volume expansion works only
when `allowVolumeExpansion` is true.

## Trade-offs
- Data lives on one node; losing the node loses the volume. Use for replicated apps (databases
  with their own replication, Kafka, Elasticsearch). TopoLVM snapshots can be restored only on the
  same node as the source volume.
- Pods are pinned to their node; draining needs the app to rebuild elsewhere.

## Verify
```bash
kubectl get csistoragecapacities -A
kubectl get pvc -o wide   # then list logical volumes on the node with the LVM tools
```
Each PVC has a matching LV on the pod's node.

## Checked

Checked 2026-10-27. Documentation checked: TopoLVM docs and Helm chart (topolvm/topolvm main: advanced-setup, lvmd, design, limitations, chart README and templates), OpenEBS lvm-localpv docs (develop: storageclasses.md, quickstart.md), Kubernetes website main tree storage capacity page (v1.38 dev; v1.37 latest release). Confirmed: `pvcreate`/`vgcreate` node preparation, chart `lvmd.deviceClasses` keys `name`, `volume-group`, `default`, `spare-gb` (default 10), StorageClass rendered with provisioner `topolvm.io` and `csi.storage.k8s.io/fstype`, `WaitForFirstConsumer` recommendation, storage capacity tracking enabled by default, same-node snapshot restore limitation, OpenEBS `local.csi.openebs.io`, `storage: lvm`, `volgroup`/`vgpattern`, `fsType` list, `allowVolumeExpansion`. Fixed: the TopoLVM StorageClass was shown with a parameter key the documentation does not state; it now follows the chart values. Removed as unconfirmed: the `topolvm.io/device-class` parameter key and the `lvs` over ssh check.

Method: documentation only; no commands were run.
