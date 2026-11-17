---
id: computing-software.cloud-infrastructure-engineering.openebs.kubernetes-storage-concepts-for-openebs
name: kubernetes-storage-concepts-for-openebs
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [kubernetes, csi, storageclass, pvc, pv, statefulset, rbac, personas]
level: intro
status: docs-checked
description: "Refresh the Kubernetes storage objects OpenEBS builds on (CSI, StorageClass, PVC, PV, StatefulSet) and the split between cluster administrator and application owner roles."
sources:
  - https://openebs.io/docs/concepts/basics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OpenEBS plugs into standard Kubernetes storage abstractions, so a reader needs these five:

- **CSI** is the standard through which providers like OpenEBS expose storage. Installing OpenEBS installs its CSI driver components.
- **StorageClass and dynamic provisioning.** A StorageClass describes a class of storage, and dynamic provisioning creates storage on request so administrators need not pre-provision. OpenEBS ships default StorageClasses for local and replicated volumes; the administrator enables the engines needed and creates classes for them.
- **PersistentVolumeClaim**: a user's request for size and access mode, served by a StorageClass.
- **PersistentVolume**: created by the provider for the claim; Kubernetes uses it to attach and mount the storage.
- **StatefulSets and Deployments**: workloads reference a PVC that names the StorageClass.

The docs define two personas. **Cluster administrators** (platform SREs) manage the cluster lifecycle, install OpenEBS and configure the StorageClasses. **Application owners** have access to specific namespaces, may view but not edit StorageClasses, and manage objects such as Deployments, StatefulSets, ConfigMaps and PVCs. Finer roles use Kubernetes RBAC.

Cluster design guidance on this page: Kubernetes 1.23 or higher is recommended; install the ext4, xfs, nfs, lvm, zfs or nvme packages the chosen engine needs; prepare devices (no filesystem, or an LVM volume group or ZFS pool); and expect extra steps on managed platforms such as AKS, Rancher, OpenShift or GKE. Choose between hyperconverged (apps and storage co-located) and separate node pools.

## Checked

Method: 2026-11-08 read the raw markdown of the cited concepts page in full; all claims were already supported and are unchanged. Added the managed-platform names and the hyperconverged versus separate-pools choice from the page.
