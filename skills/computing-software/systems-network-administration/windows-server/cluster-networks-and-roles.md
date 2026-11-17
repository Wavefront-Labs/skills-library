---
id: computing-software.systems-network-administration.windows-server.cluster-networks-and-roles
name: cluster-networks-and-roles
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, cluster-networks, cluster-roles, network-role, live-migration-network, cluster-heartbeat, preferred-owners]
level: practitioner
status: docs-checked
description: "Configure failover cluster networks (cluster-only, client, none), live migration network choice, heartbeat thresholds and role preferred owners."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/failover-cluster-network-recommendations
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/smb-multichannel
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-affinity
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clusterownernode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster networks and roles

## Network roles
```powershell
Get-ClusterNetwork | Select Name,Role,Address,Metric,AutoMetric
(Get-ClusterNetwork 'Cluster Network 2').Name = 'Storage'
(Get-ClusterNetwork 'Storage').Role = 0         # 0 none, 1 cluster only, 3 cluster and client
(Get-ClusterNetwork 'Management').Role = 3
```
- Use at least two networks for failover clustering; all networks that are found are used for cluster heartbeats.
- Role values: 0 = no cluster use, 1 = cluster only, 3 = cluster and client.

## Live migration
```powershell
Get-ClusterResourceType 'Virtual Machine' | Set-ClusterParameter -Name MigrationExcludeNetworks `
  -Value ([string]::Join(';',(Get-ClusterNetwork | ? Name -ne 'LiveMigration').ID))
Set-VMHost -VirtualMachineMigrationPerformanceOption SMB
```

## Heartbeat thresholds
```powershell
Get-Cluster | Select SameSubnetDelay,SameSubnetThreshold,CrossSubnetDelay,CrossSubnetThreshold
(Get-Cluster).SameSubnetThreshold = 20    # raise for flaky networks only after fixing the cause
```

## Roles: owners and failover policy
```powershell
Set-ClusterOwnerNode -Group 'FS01' -Owners NODE1,NODE2
Move-ClusterGroup 'FS01' -Node NODE2
```
- Anti-affinity (`AntiAffinityClassNames`; Windows Server 2022+: affinity rules
  `New-ClusterAffinityRule`) keeps replicas of a service on different nodes.
- Preferred owners are set per group and possible owners per resource (`Set-ClusterOwnerNode -Group` / `-Resource`).

## Verify
- [ ] `Get-ClusterNetworkInterface` all Up.
- [ ] Planned move of each role to each preferred node succeeds.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (Hyper-V failover-cluster-network-recommendations for Role values 0, 1 and 3, smb-multichannel and the Cluster-Affinity article, repository last commit 2026-10-23) and the Windows Server 2022/2025 PowerShell reference (plus the Set-VMHost reference and the support article on heartbeat settings): MigrationExcludeNetworks, Set-VMHost -VirtualMachineMigrationPerformanceOption values (Compression, SMB), SameSubnetThreshold and related property names, two-or-more-networks guidance, Role property values, Set-ClusterOwnerNode -Group/-Resource, AntiAffinityClassNames and New-ClusterAffinityRule (cmdlets exist only in the 2022 and 2025 sets). Removed unconfirmed role-value commentary on iSCSI and metrics, default heartbeat thresholds, Hyper-V threshold, group failover and failback property values, the SMB/Compression remark, and the dead sources entries (failover-cluster-networking-basics and configure-failover-cluster-role-settings are not in the docs repository).

Method: documentation only; no commands were run.
