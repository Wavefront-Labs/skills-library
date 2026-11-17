---
id: computing-software.systems-network-administration.windows-server.cluster-os-rolling-upgrade
name: cluster-os-rolling-upgrade
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, cluster-rolling-upgrade, update-clusterfunctionallevel, mixed-mode, cluster-functional-level, in-place-upgrade]
level: advanced
status: docs-checked
description: "Upgrade a failover cluster's OS node by node with Cluster OS Rolling Upgrade: mixed-mode limits, evict-reinstall vs in-place, and raising the cluster functional level."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-operating-system-rolling-upgrade
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/update-clusterfunctionallevel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster OS rolling upgrade

Upgrade a Hyper-V or SOFS cluster to the next Windows Server version without downtime
for the workloads. Upgrade one OS version at a time (for example 2022 to 2025); to skip versions run the upgrades sequentially or migrate to
a new cluster. In-place upgrade of a node is supported as well as clean install, if you resolve all warnings.

## Per node
```powershell
Suspend-ClusterNode NODE1 -Drain -Wait
# Option A (classic): evict, clean install new OS, rejoin
Remove-ClusterNode NODE1 -Force
# ... reinstall, install features, configure networking identically
Add-ClusterNode -Cluster CLUSTER01 -Name NODE1
# Option B: in-place upgrade while paused (resolve upgrade warnings first)
Resume-ClusterNode NODE1 -Failback Immediate
```
Repeat for every node. Back up the cluster configuration and workloads first.

## Mixed-mode rules
- While nodes run different OS versions the cluster stays at the old functional level:
  new features are unavailable.
- Manage the cluster from a node running the newer OS.
- Avoid creating or resizing storage on newer nodes in mixed mode: failing over from a newer to an older node can hit
  incompatibilities.
- Finish within four weeks; Hyper-V and SOFS clusters can be upgraded in a few hours with no downtime.
- The process is reversible until you update the cluster functional level.

## Finish
```powershell
Get-Cluster | Select ClusterFunctionalLevel,ClusterUpgradeVersion
Update-ClusterFunctionalLevel           # irreversible
Update-StoragePool -FriendlyName <pool>  # storage pool version, without downtime
Get-VM | Update-VMVersion               # per VM when shut down
```
VMs older than configuration version 8.0 cannot run on a Windows Server 2022 or newer cluster until upgraded.

## Gotchas
- Raising the functional level is one-way; nodes with the old OS can no longer join.
- Check third-party backup and monitoring agents support the new version before starting.

## Verify
- [ ] ClusterFunctionalLevel matches the new OS; all nodes Up.

## Checked

Confirmed 2026-10-25 against the Cluster OS Rolling Upgrade article (ms.date 2025-03-19, repository last commit 2026-10-23): one-version-at-a-time rule, in-place and clean-install options, mixed-OS limits and the four-week recommendation, reversibility until Update-ClusterFunctionalLevel, irreversible functional level and storage pool update, VM configuration version 8.0 requirement. Removed unconfirmed claims about live migration direction, quorum and role restrictions and third-party agent notes.

Method: documentation only; no commands were run.
