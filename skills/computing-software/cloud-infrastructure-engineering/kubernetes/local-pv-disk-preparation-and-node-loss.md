---
id: computing-software.cloud-infrastructure-engineering.kubernetes.local-pv-disk-preparation-and-node-loss
name: local-pv-disk-preparation-and-node-loss
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-persistent-volumes, disk-prep, local-disk-setup, local-pv-node-loss, local-static-provisioner, nvme]
level: advanced
status: docs-checked
description: "Prepare node disks for local PVs (format, mount by UUID, static provisioner discovery) and recover when a node dies and its pods are stuck Pending."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#local", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/node-cleanup-controller.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local PVs: disk preparation and node loss

## Prepare disks (per node)
The local-volume plugin expects stable paths across reboots. The static provisioner discovers mount points (Filesystem mode) or symbolic links (Block mode) in a discovery directory (`hostDir`, one directory per storage class).
```bash
sudo mkdir -p /mnt/disks
sudo mkfs.ext4 /dev/path/to/disk
DISK_UUID=$(sudo blkid -s UUID -o value /dev/path/to/disk)
sudo mkdir /mnt/disks/$DISK_UUID
sudo mount -t ext4 /dev/path/to/disk /mnt/disks/$DISK_UUID
echo UUID=$DISK_UUID /mnt/disks/$DISK_UUID ext4 defaults 0 2 | sudo tee -a /etc/fstab
```
- Best practice: use the UUID both in the fstab entry and in the mount directory name, so the wrong volume is never mounted after a device path change and a recreated node with the same name does not look like the old one.
- For IO isolation use a whole disk per volume; for capacity isolation use a partition per volume. Directories sharing one filesystem can be bind-mounted into the discovery directory but do not isolate capacity.
- Raw block volumes: leave the device unformatted and symlink it into the discovery directory using a unique name (for example from `/dev/disk/by-id/`); the class needs `volumeMode: Block`.
- Avoid recreating nodes with the same name while old PVs with that node's affinity still exist.

## Discovery: local static provisioner
Helm values define classes (the chart's `values.yaml` uses `classes:` with `hostDir`, `volumeMode`, `fsType`, `namePattern` and a `storageClass` section with `reclaimPolicy` of `Delete` or `Retain` and `isDefaultClass`):
```yaml
classes:
- name: fast-disks
  hostDir: /mnt/fast-disks
  volumeMode: Filesystem
  fsType: ext4
  storageClass:
    reclaimPolicy: Delete
```
It creates one PV per discovered volume with node affinity to that node. The StorageClass uses `provisioner: kubernetes.io/no-provisioner` and `volumeBindingMode: WaitForFirstConsumer`. Block devices are cleaned with a configurable cleaner command (default `/scripts/quick_reset.sh`).

## Decommissioning a disk
Stop Pods using it, remove it from the node (unmount, remove the fstab entry), delete the PVC; the provisioner's cleanup will fail because the volume is gone, so delete the PV object manually.

## Node loss
A Pod bound to a local PV can only run on that node; if the node is lost, the Pod cannot run (`didn't match PersistentVolume's node affinity`). For replicated applications, after confirming the node and disk are gone:
```bash
kubectl delete pvc data-kafka-2 --wait=false
kubectl delete pv <local-pv-of-dead-node>
kubectl delete pod kafka-2
```
The StatefulSet recreates the PVC, which binds a free local PV on another node; the application then re-replicates (decommission the old member first if the application requires it).

The provisioner project also ships a node cleanup controller that removes PVs and PVCs referencing deleted Node objects. It does not clean disk data, only API objects, and a StatefulSet must back the Pods for them to be rescheduled automatically. By default it handles PVs of type `local`; CSI node-local drivers need `--storageclass-names` and `--csi-drivers`. Deploy it only if deleting a Node object reliably means the data is lost.

## Verify
- [ ] After a reboot all mounts under the discovery directory are present (`findmnt`).
- [ ] A game-day node termination recovers on another node following this runbook.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: UUID mount practice, isolation guidance, discovery directory rules, chart values keys, node cleanup controller behaviour.

Method: documentation only; no commands were run.
