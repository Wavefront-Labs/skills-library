---
id: computing-software.systems-network-administration.virtualisation.cluster-os-rolling-upgrade
name: cluster-os-rolling-upgrade
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [cluster-os-rolling-upgrade, cluster-functional-level, failover-clustering, hyper-v-cluster, vm-configuration-version, hyper-v]
level: advanced
status: docs-checked
description: "Upgrade a Hyper-V failover cluster to a newer Windows Server without downtime: drain, upgrade or clean install, rejoin in mixed-OS mode, raise the functional level."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-operating-system-rolling-upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster OS Rolling Upgrade

Supported one OS version at a time (for example 2022 to 2025). To span several versions, repeat the process for each
version in sequence, or migrate to a new cluster. While nodes run different versions the cluster is in
**mixed-OS mode** and stays fully functional; VMs keep running.

## Prepare
- Back up VMs and the cluster configuration (a System State backup lets you roll back the functional level later).
- Capacity to run all VMs with one node out.
- Firmware, drivers and NIC/HBA support for the new OS.
- VM configuration versions older than 8.0 cannot run on a Windows Server 2022 or newer cluster: plan to upgrade
  them (see below).

## Per node
```powershell
Suspend-ClusterNode -Name hv01 -Drain
Remove-ClusterNode -Name hv01          # evict: only for a clean install
```
Then upgrade in place, or clean install the new Windows Server on the node. For a clean install: join the same
domain, use the same computer name if the cluster uses Storage Spaces Direct, install Hyper-V and Failover
Clustering, recreate virtual switches (use Switch Embedded Teaming if an LBFO team was removed), then rejoin:
```powershell
Add-ClusterNode -Name hv01
```
An in-place upgrade needs no eviction and no rejoin. Move VMs back and repeat for the next node.

## Finish
```powershell
Get-Cluster | Select ClusterFunctionalLevel
Update-ClusterFunctionalLevel        # all nodes must be up and in active membership
Update-StoragePool -FriendlyName '<pool name>'     # if you use storage pools
```
Then, in a maintenance window with VMs off, upgrade VM configuration versions:
```powershell
Update-VMVersion -Name app01
Get-VM | Select Name, Version
```

## Gotchas
- Mixed-OS mode is transitory: Microsoft recommends finishing within four weeks, and new features stay unavailable
  until the functional level is raised.
- Rolling back after `Update-ClusterFunctionalLevel` needs an authoritative restore from a System State backup
  taken beforehand.
- In mixed-OS mode manage the cluster from a node running the newer Windows Server.
- VMs upgraded to a newer configuration version cannot run on older hosts: upgrade VM versions last.

## Verify
All nodes on the new build, `ClusterFunctionalLevel` updated, `Test-Cluster` clean, VMs on the new configuration
version and migrating freely.

## Checked

Date checked: 2026-10-27. Documentation: Windows Server failover clustering "Cluster operating system rolling upgrade" page (windowsserverdocs main branch, covers Windows Server 2022 and 2025).
Confirmed: one-version-at-a-time rule; four-week mixed-OS guidance; Suspend-ClusterNode -Drain, Remove-ClusterNode (clean install only), Add-ClusterNode, Update-ClusterFunctionalLevel (all nodes on and in active membership), Update-StoragePool, Update-VMVersion; VM configuration version 8.0 minimum on Windows Server 2022 and newer; manage from the newer node; rollback by System State authoritative restore; same computer name for Storage Spaces Direct clean installs.

Method: documentation only; no commands were run.
