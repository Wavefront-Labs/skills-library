---
id: computing-software.cloud-infrastructure-engineering.velero.restore-persistent-volumes
name: restore-persistent-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [restore-pv, pv-rename, velero-clone, original-pv-name, pvc-restore]
level: advanced
status: docs-checked
description: "How Velero restores PVs per backup method, renames a PV to velero-clone-UUID when namespace is remapped, and cleans PVC binding fields."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero restores a PV one of three ways depending on how the backup was taken:
1. Snapshot: Velero statically creates the PV and binds it to the restored PVC. The plugin returns a `volumeID` that is written to the PV.
2. File System Backup: the PVC is created and Kubernetes dynamic provisioning creates the PV; Velero does not create it.
3. CSI: Velero creates a PVC whose `DataSource` refers to the CSI VolumeSnapshot, taken from the annotation `velero.io/volume-snapshot-name`.

PV rename and remap applies only to the snapshot case. Velero renames a PV when both hold: the PV already exists on the target cluster, and the claim namespace has been remapped. The new name is `velero-clone-` plus a random UUID, and the original is kept in annotation `velero.io/original-pv-name`. If you restore into the original namespace without remapping, no rename happens, and if the PVC already exists the PV creation fails with `Already Exist`.

PVC changes: for dynamically bound PVCs Velero removes `volumeName` and the annotations `pv.kubernetes.io/bind-completed` and `pv.kubernetes.io/bound-by-controller`, so default binding works. It also removes `volume.kubernetes.io/selected-node` so `WaitForFirstConsumer` and topology rules apply. If the PV was renamed, the PVC `volumeName` is updated to match.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Restoring Persistent Volumes and Persistent Volume Claims" subsections, read in full). All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
