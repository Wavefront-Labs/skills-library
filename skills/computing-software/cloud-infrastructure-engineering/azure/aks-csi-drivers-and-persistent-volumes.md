---
id: computing-software.cloud-infrastructure-engineering.azure.aks-csi-drivers-and-persistent-volumes
name: aks-csi-drivers-and-persistent-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-storage, csi-drivers, persistent-volumes, azure-disk-csi, azure-files-csi, blob-csi, storageclass]
level: practitioner
status: docs-checked
description: "Choose and configure AKS storage: Azure Disk, Files and Blob CSI drivers, built-in and custom StorageClasses, zone-aware disks, snapshots, expansion and reclaim policies."
sources: ["https://learn.microsoft.com/azure/aks/csi-storage-drivers", "https://learn.microsoft.com/azure/aks/create-volume-azure-disk", "https://learn.microsoft.com/azure/aks/create-volume-azure-files", "https://learn.microsoft.com/azure/aks/concepts-storage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS CSI drivers and persistent volumes

**Goal:** stateful pods get the right storage type, survive node and zone events, and volumes
are expandable and backed up.

## Pick the driver
| Need | Driver / class | Access |
|---|---|---|
| Single-pod DB, low latency | Azure Disk `managed-csi-premium` (Premium SSD ZRS/LRS), Premium SSD v2 custom class | RWO |
| Shared files across pods | Azure Files `azurefile-csi-premium` (SMB) or NFS class | RWX |
| Large object data, analytics | Blob CSI (`azureblob-nfs-premium` or `azureblob-fuse-premium`) | RWX |
| Ephemeral fast scratch | Ephemeral OS disk / `emptyDir` / Azure Container Storage | — |
Since Kubernetes 1.21 AKS uses CSI drivers by default (existing in-tree volumes keep working through CSI migration). Enable a driver on an existing cluster with `az aks update --enable-disk-driver`, `--enable-file-driver` or `--enable-blob-driver`.

## Built-in classes worth knowing
Disk: `default` (Standard SSD), `managed-csi` (Standard SSD LRS), `managed-csi-premium` (Premium SSD) and, on Kubernetes 1.35 and later, `managed-csi-premium-v2` (Premium SSD v2, LRS). Files: `azurefile-csi` (HDD) and `azurefile-csi-premium` (SSD). Blob: `azureblob-fuse-premium` and `azureblob-nfs-premium`.
From Kubernetes 1.29, on clusters deployed across availability zones the built-in disk classes (except `managed-csi-premium-v2`) create zone-redundant (ZRS) disks, which cost more than LRS. The Files classes use `reclaimPolicy: Delete`, so deleting the PV deletes the file share; delete the PVC rather than the PV.

## Custom class (zone-redundant premium, retain, expandable)
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: { name: premium-zrs-retain }
provisioner: disk.csi.azure.com
parameters: { skuName: Premium_ZRS, cachingMode: ReadOnly }
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```
`WaitForFirstConsumer` delays provisioning until a pod uses the claim, so the disk is created in a zone the pod can run in (with topology-constrained node pools, `Immediate` binding can pick a zone the pod cannot use). ZRS replicates the disk synchronously across zones.

## Expand and snapshot
```bash
kubectl patch pvc data-pg-0 -p '{"spec":{"resources":{"requests":{"storage":"256Gi"}}}}'
```
Disk expansion needs `allowVolumeExpansion: true` and works without downtime up to 4 TiB (beyond that, Standard HDD/SSD and Premium SSD volumes must be detached first; Premium SSD v2 and Ultra Disk support online expansion). The Files classes are expandable by editing the PVC. Snapshots: `VolumeSnapshotClass` with `driver: disk.csi.azure.com`; the `incremental` parameter defaults to `true`.

## Static provisioning (existing disk/share)
PV with `csi.volumeHandle` set to the disk resource ID. Create the disk in the node resource group so the cluster can manage it; if it lives in another resource group, grant the cluster's managed identity the `Contributor` role on that resource group.

## Gotchas
- The number of data disks a node can attach depends on its VM size; pods that need more stay Pending.
- The Azure Files CSI driver mounts SMB shares only with key-based (NTLM v2) authentication; NFS shares do not need keys.
- Deleting a namespace with a `Delete` reclaim policy deletes the data - use `Retain` for production databases.
- Premium SSD v2 supports only `cachingMode: None` and has region and zone availability requirements; check that your node pool zones support it.

## Verify
- [ ] `kubectl get pvc -A` all Bound; `kubectl describe pv` shows expected `skuName` and zone.
- [ ] Drain a node: the stateful pod reschedules and remounts its volume.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (csi-storage-drivers, create-volume-azure-disk, create-volume-azure-files, concepts-storage; main branch).
- Confirmed: CSI default since 1.21; `--enable-disk-driver`/`--enable-file-driver`/`--enable-blob-driver`; built-in class names and backing media; ZRS default for built-in disk classes on zonal clusters from 1.29; `managed-csi-premium-v2` from 1.35; `Premium_ZRS` as a `skuName` value; `WaitForFirstConsumer` behaviour; expansion limits; snapshot `incremental` default; Contributor role for disks in a separate resource group; Premium SSD v2 caching limit; Files SMB key-based authentication.
- Removed as unconfirmed: the per-VM-size disk count example, the Azure Backup for AKS remark, managed-identity Files mounting, and the claim that LRS pods cannot change zone.
Method: documentation only; no commands were run.
