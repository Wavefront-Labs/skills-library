---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-quorum-and-witness
name: hyper-v-cluster-quorum-and-witness
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, cluster-quorum, cloud-witness, file-share-witness, disk-witness, dynamic-quorum, failover-clustering, windows-server]
level: advanced
status: docs-checked
description: "Configure failover cluster quorum for Hyper-V: cloud, file share or disk witness, dynamic quorum and witness weight, and two-node and stretched-cluster considerations."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/what-is-quorum-witness
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/deploy-quorum-witness
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clusterquorum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cluster quorum and witness options

**Goal:** keep the cluster running through node and site failures without split-brain.

## Witness choices
| Witness | Use |
|---|---|
| Cloud witness (Azure Storage blob) | No third datacenter needed; needs an Azure general purpose v2 storage account |
| File share witness | SMB share outside the cluster; a domain-joined Windows server in the same forest, or (Windows Server 2019 or later) a non-domain device such as NAS or a router with USB storage |
| Disk witness | Small shared disk visible to all nodes |

```powershell
Set-ClusterQuorum -CloudWitness -AccountName 'stclwitness' -AccessKey $key
Set-ClusterQuorum -FileShareWitness '\\fs01\ClusterWitness$'
Set-ClusterQuorum -DiskWitness 'Cluster Disk 5'
Get-ClusterQuorum
```
Configure the quorum so the number of voting elements is odd: with an even number of voting nodes add a witness.

## Dynamic quorum
Dynamic quorum management adjusts quorum majority requirements so the cluster can keep running as nodes are shut down one at a time, down to the last node. It does not let the cluster survive the simultaneous failure of most voting members, and if you explicitly remove a node's vote the cluster cannot add or remove that vote dynamically.
```powershell
Get-ClusterNode | Format-Table Name, State, NodeWeight, DynamicWeight   # DynamicWeight 0 = no vote right now
```

## Two-node and stretched clusters
Always configure a witness on a two-node cluster. For multisite clusters the cloud witness removes the need for a third site; removing votes from nodes in a backup site is for specific disaster recovery designs only.

## Gotchas
- Cloud witness uses HTTPS port 443 to the `.core.windows.net` endpoint: allow it through every firewall between the nodes and Azure Storage.
- Restart the cluster service on the last active node before shutting down all nodes when using a file share or cloud witness, as the docs advise.

## Verify
Stop the cluster service on one node at a time (in maintenance) and confirm the cluster stays up; `Get-ClusterQuorum` shows the witness online.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the quorum witness pages: disk, file share and cloud witness types; a witness is recommended when the node count is even; dynamic quorum management lets the cluster run down to the last node and cannot dynamically change a vote you removed; cloud witness needs a general purpose v2 storage account and outbound HTTPS on port 443 to the .core.windows.net endpoint; a file share witness on a non-domain-joined device needs Windows Server 2019 or later and can be a NAS or a router with local USB storage; the Set-ClusterQuorum syntax. Removed as unconfirmed: the WitnessDynamicWeight and LowerQuorumPriorityNodeID properties, the dynamic witness version gate, and the rule against hosting the witness on a cluster VM.

Method: documentation only; no commands were run.
