---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vm-groups
name: hyper-v-vm-groups
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-group, hyper-v, vm-collections, cluster-sets]
level: practitioner
status: docs-checked
description: "Group Hyper-V VMs with VM groups (VM collections and management collections) for bulk operations and backup, and use cluster group sets for start ordering."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmgroup
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-clustergroupset
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clustergroupset
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM groups

**Goal:** treat multi-VM applications as a unit for management, backup and startup order.

## Hyper-V VM groups
- **VMCollectionType**: a set of VMs (for example the tiers of one application).
- **ManagementCollectionType**: a group of VM collections (VMCollectionType groups).
```powershell
New-VMGroup -Name 'erp-app' -GroupType VMCollectionType
Add-VMGroupMember -VMGroup (Get-VMGroup 'erp-app') -VM (Get-VM 'erp-web*','erp-app*','erp-db*')
New-VMGroup -Name 'finance' -GroupType ManagementCollectionType
Add-VMGroupMember -VMGroup (Get-VMGroup 'finance') -VMGroupMember (Get-VMGroup 'erp-app')
Get-VMGroup 'erp-app' | Select -ExpandProperty VMMembers | Stop-VM
```

## Cluster start ordering: group sets
For start ordering in a failover cluster use **cluster group sets**, which let you control when sets start through dependencies between sets:
```powershell
New-ClusterGroupSet -Name 'erp-db'  ; Add-ClusterGroupToSet -Name 'erp-db'  -Group 'erp-db01'
New-ClusterGroupSet -Name 'erp-app' ; Add-ClusterGroupToSet -Name 'erp-app' -Group 'erp-app01','erp-app02'
Add-ClusterGroupSetDependency -Name 'erp-app' -Provider 'erp-db'
Set-ClusterGroupSet -Name 'erp-db' -StartupDelayTrigger Online -StartupDelay 60     # StartupDelay: seconds after the set is ready
```

## Gotchas
- A VMCollectionType group holds VMs; a ManagementCollectionType group holds VMCollectionType groups.
- `StartupDelayTrigger` is an alias of `-StartupSetting`, which accepts `Delay` or `Online`.

## Verify
`Get-VMGroup | Select Name, GroupType, VMMembers`; after a cluster cold start, `Get-ClusterGroupSet` order is respected (DB online before app).

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: New-VMGroup -GroupType accepts VMCollectionType and ManagementCollectionType, a management collection contains VM collection groups, Add-VMGroupMember; New-ClusterGroupSet, Add-ClusterGroupSetDependency -Provider, Set-ClusterGroupSet -StartupDelay and the StartupSetting parameter with alias StartupDelayTrigger (Delay or Online). Corrected: a management collection holds VM collections, not other management collections. Removed as unconfirmed: the Windows Server 2016 gate, backup vendor use, host-local and VM ID statements, and the claim that VM groups never affect start order.

Method: documentation only; no commands were run.
