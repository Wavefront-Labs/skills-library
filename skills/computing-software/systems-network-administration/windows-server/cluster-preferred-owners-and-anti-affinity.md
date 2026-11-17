---
id: computing-software.systems-network-administration.windows-server.cluster-preferred-owners-and-anti-affinity
name: cluster-preferred-owners-and-anti-affinity
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, preferred-owners, anti-affinity, possible-owners, failback]
level: advanced
status: docs-checked
description: "Control where clustered roles run: preferred and possible owners, anti-affinity class names and 2022+ affinity rules, and how they interact."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-affinity
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clusterownernode
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-clusteraffinityrule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster preferred owners and anti-affinity

## Preferred owners (group level)
Ordered list of nodes a role prefers.
```powershell
Set-ClusterOwnerNode -Group SQL-AG1 -Owners NODE1,NODE2
Get-ClusterOwnerNode -Group SQL-AG1
```
Preferred owners can be combined with anti-affinity in clusters of three or more nodes.

## Possible owners (resource level)
Nodes allowed to host a resource at all. Use `-Resource`/pipeline form to set them per resource.
```powershell
Get-ClusterResource 'SQL IP Address 1' | Set-ClusterOwnerNode -Owners NODE1,NODE2
```

## Keep roles apart
- **AntiAffinityClassNames** (soft): roles sharing a class name avoid the same node when possible.
```powershell
$v = New-Object System.Collections.Specialized.StringCollection; $v.Add('DCs') | Out-Null
(Get-ClusterGroup DC01).AntiAffinityClassNames = $v
(Get-ClusterGroup DC02).AntiAffinityClassNames = $v
```
- **Affinity rules** (Windows Server 2022 and later): `New-ClusterAffinityRule -Name SplitDCs -RuleType DifferentNode` (or SameNode,
  SameFaultDomain, DifferentFaultDomain), `Add-ClusterGroupToAffinityRule`, `Set-ClusterAffinityRule -Enabled 1`.
- `(Get-Cluster).ClusterEnforcedAntiAffinity = 1` turns AntiAffinityClassNames into a hard block: the second role goes
  offline (Anti-Affinity Conflict) rather than share a node. Both settings apply only after the roles are recycled.

## Caution
With ClusterEnforcedAntiAffinity on a two-node cluster, if one node is down both roles will not run.

## Verify
- [ ] Draining a node puts each role where expected (`Suspend-ClusterNode -Drain`, then `Get-ClusterGroup | ft Name,OwnerNode`).

## Checked

Confirmed 2026-10-25 against the Cluster-Affinity article (repository last commit 2026-10-23) and the Windows Server 2022/2025 PowerShell reference: AntiAffinityClassNames as a soft block, ClusterEnforcedAntiAffinity as a hard block, the Anti-Affinity Conflict state, two-node caveat, New-ClusterAffinityRule RuleType values (SameFaultDomain, SameNode, DifferentFaultDomain, DifferentNode), Set-ClusterOwnerNode parameters. Removed unconfirmed failback property values and the claimed evaluation order of owner lists and affinity.

Method: documentation only; no commands were run.
