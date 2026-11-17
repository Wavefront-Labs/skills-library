---
id: computing-software.systems-network-administration.windows-server.cluster-quorum-and-witness
name: cluster-quorum-and-witness
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, cluster-quorum, cloud-witness, file-share-witness, disk-witness, dynamic-quorum, set-clusterquorum]
level: practitioner
status: docs-checked
description: "Configure failover cluster quorum: dynamic quorum and witness types (cloud, file share, disk), choosing per topology, Set-ClusterQuorum and forcing quorum in a disaster."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/what-is-quorum-witness
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/deploy-quorum-witness
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/file-share-witness
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/recover-failover-cluster-without-quorum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster quorum and witness configuration

## Model
Each node has a vote; a witness adds one. The cluster runs while a majority of votes is present. Dynamic quorum
adjusts the majority requirement as nodes shut down; check a node's `DynamicWeight` (0 = no vote, 1 = vote).
Configure a witness when the cluster has an even number of voting nodes, and aim for an odd number of votes.

## Which witness
| Witness | Use |
|---|---|
| Cloud witness (Azure blob) | default choice; multi-site; no third site needed |
| File share witness | no Azure; preferred for multisite clusters with replicated storage, hosted at a third site; routers with local USB storage are a listed option. DFS or replicated storage for the witness share is not supported |
| Disk witness | shared disk reachable by all nodes; typically recommended when every node can reach it |
S2D clusters cannot use a disk witness.

## Configure
```powershell
# Cloud witness (Standard general-purpose v2 storage account; LRS when on-premises or in one Azure region)
Set-ClusterQuorum -CloudWitness -AccountName stclwitness01 -AccessKey <key> -Endpoint core.windows.net
# File share witness (CNO needs Full Control on share and NTFS)
Set-ClusterQuorum -FileShareWitness '\\fs01\ClusterWitness$\CLUSTER01'
# Disk witness
Set-ClusterQuorum -DiskWitness 'Cluster Disk 5'
Get-ClusterQuorum
Get-ClusterNode | Select Name,NodeWeight,DynamicWeight
```
Outbound HTTPS 443 to the blob endpoint is required for the cloud witness.

## Multi-site tips
- Remove votes from DR nodes that should never form quorum alone:
  `(Get-ClusterNode NODE5).NodeWeight = 0`.
- Prefer witness in a third location so either site can survive.

## Disaster: force quorum
Only when you are sure the other half is down:
```powershell
Start-ClusterNode -Name NODE3 -ForceQuorum
Start-ClusterNode -Name NODE1 -PreventQuorum   # other nodes: join the running cluster instead of forming a new one
```
While forced, quorum settings are ignored; the cluster leaves the forced state automatically once it regains enough votes.
Start the remaining nodes with `-PreventQuorum` so they join the running cluster instead of forming a competing one.

## Verify
- [ ] `Get-ClusterQuorum` shows the witness; witness resource Online.
- [ ] Event 1177/1135 history reviewed.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (what-is-quorum-witness, deploy-quorum-witness, file-share-witness and recover-failover-cluster-without-quorum; repository last commit 2026-10-23) and the Set-ClusterQuorum and Start-ClusterNode reference (ForceQuorum with FixQuorum alias, PreventQuorum): witness guidance for even node counts, cloud witness needing a Standard general-purpose v2 account and port 443, no disk witness for Storage Spaces Direct, USB on routers, DynamicWeight, forcing quorum and PreventQuorum. Removed unconfirmed LowerQuorumPriorityNodeID, the 1 GB disk size, the net start command and the authoritative-configuration claim.

Method: documentation only; no commands were run.
