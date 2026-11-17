---
id: computing-software.cloud-infrastructure-engineering.velero.restore-order-priorities
name: restore-order-priorities
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [restore-order, restore-resource-priorities, velero-server, customresourcedefinitions, restore-priority]
level: advanced
status: docs-checked
description: "Know the default Velero restore order and customise it with the server flag --restore-resource-priorities and its hyphen separator."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero restores resources in a fixed default order, starting: CustomResourceDefinitions, Namespaces, StorageClasses, VolumeSnapshotClass, VolumeSnapshotContents, VolumeSnapshots, DataUploads, PersistentVolumes, PersistentVolumeClaims, ClusterRoles, Roles, ServiceAccounts, ClusterRoleBindings, RoleBindings, Secrets, ConfigMaps, LimitRanges, PriorityClasses, Pods, ReplicaSets, ClusterClasses, Endpoints, Services, ClusterBootstraps, Clusters, ClusterResourceSets, Apps, PackageInstalls.

The docs recommend keeping the default. To change it for all future restores, set `--restore-resource-priorities` on the Velero server. You need not list every resource. The list has two parts split by a `-` element:
- Entries before `-` are restored first (high priority).
- Entries after `-` are restored last (low priority).
- Anything not listed is restored alphabetically between the two groups.

Example fragment using fully qualified names:

```shell
velero server \
--restore-resource-priorities=customresourcedefinitions,namespaces,storageclasses,\
persistentvolumes,persistentvolumeclaims,secrets,configmaps,pods,replicasets.apps,\
endpoints,services,-,clusters.cluster.x-k8s.io
```

The customised order applies to all future restores.

Related behaviour: after creating a CRD, the restore waits up to 1 minute for it to become available, and after a Pod it runs restore hooks and waits for them.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page (raw markdown, read in full): default restore order, the `--restore-resource-priorities` server flag and its `-` split, the 1 minute CRD wait and Pod hook wait. Removed the inferred claim that the setting cannot be made per restore.

Method: documentation only; no commands were run.
