---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-node-drain
name: hyper-v-cluster-node-drain
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [suspend-clusternode, node-drain, failover-clustering, hyper-v-cluster, maintenance-mode, storage-spaces-direct, hyper-v]
level: practitioner
status: docs-checked
description: "Put a Hyper-V cluster node into maintenance with Suspend-ClusterNode -Drain, handle failed drains, S2D storage maintenance mode, and resume with failback."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/suspend-clusternode
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/resume-clusternode
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/upgrade-storage-spaces-direct
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Draining a Hyper-V cluster node

## Drain
```powershell
Suspend-ClusterNode -Name hv02 -Drain -Wait
Get-ClusterNode hv02 | Select Name, State
```
`-Drain` moves the clustered roles off the node before pausing it; `-TargetNode` picks the destination; `-Wait` makes the cmdlet wait for completion. The node-level pause is usually done when applying updates. For long diagnosis work the reference suggests stopping the cluster service instead of pausing.

## If a drain does not finish
```powershell
Get-ClusterGroup | ? OwnerNode -eq hv02 | Select Name, State
```
Fix the blocking role and rerun. `-ForceDrain` (with `-Drain`) tries to move workloads safely with the best placement; any workload that cannot be moved safely is stopped and moved to another node as a failed role, and the node is then forced to pause. Use it only after accepting that downtime.

## Storage Spaces Direct nodes
Put the node's storage into maintenance after the drain, and wait for repairs before the next node:
```powershell
Suspend-ClusterNode -Name hv02 -Drain -Wait
Get-StorageFaultDomain -Type StorageScaleUnit | ? FriendlyName -eq hv02 | Enable-StorageMaintenanceMode
# ... work, reboot ...
Get-StorageFaultDomain -Type StorageScaleUnit | ? FriendlyName -eq hv02 | Disable-StorageMaintenanceMode
Resume-ClusterNode -Name hv02
Get-StorageJob            # wait until repair jobs finish before the next node
```
Follow the current Storage Spaces Direct upgrade page for the exact sequence.

## Resume
```powershell
Resume-ClusterNode -Name hv02 -Failback Immediate     # or NoFailback / Policy
```
`Immediate` brings drained workloads back at once, `Policy` only during configured hours, `NoFailback` not at all.

## Gotchas
- Draining a two-node cluster puts all load on one node: check capacity first.

## Verify
After resume: `Get-ClusterNode` shows all nodes Up, `Get-StorageJob` is empty on S2D clusters, and VMs are placed as intended.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Suspend-ClusterNode and Resume-ClusterNode references: -Drain, -ForceDrain, -TargetNode, -Wait, and Resume-ClusterNode -Failback with NoFailback, Immediate or Policy. Confirmed in the Storage Spaces Direct upgrade page: the Suspend-ClusterNode -Drain, Get-StorageFaultDomain -Type StorageScaleUnit maintenance mode, Resume-ClusterNode and Get-StorageJob sequence. Corrected: -ForceDrain stops workloads that cannot be moved safely and moves them as failed roles, it does not quick-migrate them. Removed as unconfirmed: DrainStatus property values, the blocker list and the CAU remark.

Method: documentation only; no commands were run.
