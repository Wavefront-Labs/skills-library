---
id: computing-software.systems-network-administration.virtualisation.hyper-v-csv-cache-and-bitlocker
name: hyper-v-csv-cache-and-bitlocker
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [csv-cache, csv-bitlocker, cluster-shared-volumes, bitlocker, hyper-v]
level: advanced
status: docs-checked
description: "Configure the CSV block cache size and encrypt Cluster Shared Volumes with BitLocker using the cluster name object protector, with maintenance steps and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-manage-cluster-shared-volumes
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/bitlocker-on-csv-in-ws-2022
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CSV cache and BitLocker on CSV

**Goal:** faster reads for read-heavy VM workloads, and encryption at rest for clustered storage.

## CSV block cache
The CSV cache uses system memory to cache block-level, read-only, unbuffered I/O. It does not cache writes. Microsoft recommends it for clustered Hyper-V and Scale-Out File Server deployments.
```powershell
Get-ClusterSharedVolume | Select Name, BlockCacheSize
(Get-Cluster).BlockCacheSize = 512        # MB reserved on each node
```
- In Windows Server 2016 and later the cache is enabled by default with 1 GiB allocated; `BlockCacheSize` is a cluster common property in MB per node.
- 512 MB is described as a recommended value for many clusters. The memory comes from the host, so subtract it from what VMs can use.
- Monitor it with the **Cluster CSV Volume Cache** performance counters.

## BitLocker on CSV
1. Install the BitLocker feature on all nodes (`Install-WindowsFeature -Name BitLocker -IncludeAllSubFeature -IncludeManagementTools`, then restart).
2. Put the disk resource into maintenance mode before enabling BitLocker, or encrypt it before adding it to the cluster:
```powershell
Get-ClusterSharedVolume -Name 'Cluster Disk 2' | Suspend-ClusterResource
```
3. Enable BitLocker on the CSV mount point with a recovery password protector, then resume the resource:
```powershell
$csv = '<CSV_ROOT>\Volume1'
Enable-BitLocker -MountPoint $csv -RecoveryPasswordProtector
Get-ClusterSharedVolume -Name 'Cluster Disk 2' | Resume-ClusterResource
```
4. Save the recovery password in a secure location.

Failover Clustering requires the Active Directory-based protector for cluster disk resources in earlier Windows Server versions: an `ADAccountOrGroup` protector bound to the cluster name object (CNO), which makes unlock depend on a reachable domain controller. In Windows Server 2022 and later the cluster can instead generate and keep its own protector in the cluster database; because that database lives on every node's system volume, the page advises BitLocker-protecting the system volumes too. Follow the BitLocker on CSV page for the exact steps for your version.

## Gotchas
- Without a working protector the disk cannot come online on other nodes; if the system drive is not BitLocker protected, cluster flags a warning during online and unlock.
- Encryption runs in the background and adds I/O; schedule it.

## Verify
`Get-BitLockerVolume -MountPoint $csv` shows the protectors and *FullyEncrypted*; the CSV moves between nodes and comes online on each.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the CSV management page: the CSV cache caches block-level read-only unbuffered I/O, is enabled by default with 1 GiB in Windows Server 2016 and later, BlockCacheSize is a per-node cluster property in MB, 512 MB is a commonly recommended value, and the Cluster CSV Volume Cache counter set exists. Confirmed in the BitLocker on CSV page: BitLocker feature on all nodes, resource in maintenance mode before enabling, Suspend-ClusterResource and Resume-ClusterResource through Get-ClusterSharedVolume, Enable-BitLocker -RecoveryPasswordProtector, the older CNO (ADAccountOrGroup) protector, and the newer cluster-managed protector stored in the cluster database. Removed as unconfirmed: sizing percentages of RAM and the S2D cache remark.

Method: documentation only; no commands were run.
