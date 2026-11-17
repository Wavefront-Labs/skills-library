---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-preferred-owners-and-anti-affinity
name: hyper-v-cluster-preferred-owners-and-anti-affinity
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [preferred-owners, anti-affinity-class, failover-clustering, hyper-v-cluster, affinity-rules, hyper-v]
level: practitioner
status: docs-checked
description: "Control where clustered Hyper-V VMs run: possible and preferred owners, AntiAffinityClassNames, Windows Server 2022+ affinity rules, priority and failback settings."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-affinity
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clusterownernode
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-clusteraffinityrule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VM placement in Hyper-V failover clusters

## Owners
`Set-ClusterOwnerNode` sets which nodes can own a resource, or the order of preference among owner nodes for a role (group).
```powershell
Set-ClusterOwnerNode -Group "app01" -Owners hv01,hv02         # preferred order
Get-ClusterOwnerNode -Group "app01"
Set-ClusterOwnerNode -Resource "Virtual Machine app01" -Owners hv01,hv02,hv03   # possible owners
```

## Anti-affinity (keep pairs apart: DCs, SQL AG replicas, web farm)
Classic method with AntiAffinityClassNames (blank by default):
```powershell
$cls = New-Object System.Collections.Specialized.StringCollection; $cls.Add("DC") | Out-Null
(Get-ClusterGroup dc01).AntiAffinityClassNames = $cls
(Get-ClusterGroup dc02).AntiAffinityClassNames = $cls
(Get-Cluster).ClusterEnforcedAntiAffinity = 1     # 1 = hard block, 0 = disabled
```
AntiAffinityClassNames is a soft block: if no other node is available the groups still share a node. With `ClusterEnforcedAntiAffinity = 1` the conflicting group stays offline (shown as `Offline(Anti-Affinity Conflict)`); in a two-node cluster with one node down, both groups will not run. The settings take effect only after the resources are recycled: groups already online together keep running.

Affinity rules (the cmdlet references exist for Windows Server 2022 and later):
```powershell
New-ClusterAffinityRule -Name DCs -RuleType DifferentNode
Add-ClusterGroupToAffinityRule -Groups dc01,dc02 -Name DCs
Set-ClusterAffinityRule -Name DCs -Enabled 1
Get-ClusterAffinityRule
```
Rule types: SameNode, DifferentNode, SameFaultDomain, DifferentFaultDomain.

## Gotchas
- Preferred owners can be combined with anti-affinity in clusters of three or more nodes.

## Verify
After draining each node in turn, DC pairs never share a node (`Get-ClusterGroup | Group OwnerNode`).

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the cluster affinity page: AntiAffinityClassNames is blank by default and soft, ClusterEnforcedAntiAffinity 1 makes it a hard block, the settings take effect only after the resources are recycled, and a two-node cluster with the hard block cannot run both groups when one node is down. Confirmed in the cmdlet references: Set-ClusterOwnerNode -Group/-Resource/-Owners, and New-ClusterAffinityRule, Add-ClusterGroupToAffinityRule and Set-ClusterAffinityRule with rule types SameNode, DifferentNode, SameFaultDomain and DifferentFaultDomain; the affinity rule reference exists for Windows Server 2022 and 2025 but not 2019. Removed as unconfirmed: priority values, failback window properties, node fairness and SCVMM availability set remarks.

Method: documentation only; no commands were run.
