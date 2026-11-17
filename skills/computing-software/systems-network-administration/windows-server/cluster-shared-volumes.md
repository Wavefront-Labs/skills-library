---
id: computing-software.systems-network-administration.windows-server.cluster-shared-volumes
name: cluster-shared-volumes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, cluster-shared-volumes, csvfs, csv-redirected-io, csv-cache, add-clustersharedvolume]
level: practitioner
status: docs-checked
description: "Manage Cluster Shared Volumes: add disks to CSV, ownership balance, direct vs redirected IO, CSV block cache, maintenance mode and redirected-access troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-csvs
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-manage-cluster-shared-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/use-csv-cache
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/suspend-clusterresource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster Shared Volumes

CSV lets every node read and write the same NTFS/ReFS volume simultaneously (Hyper-V,
SOFS). One node owns metadata (coordinator); others do direct I/O to the storage.

## Add and inspect
```powershell
Get-ClusterAvailableDisk | Add-ClusterDisk
Add-ClusterSharedVolume -Name 'Cluster Disk 2'
Get-ClusterSharedVolume | Select Name,OwnerNode,State
Get-ClusterSharedVolumeState | Select Name,Node,StateInfo,FileSystemRedirectedIOReason,BlockRedirectedIOReason
```
Mount points: `ClusterStorage\VolumeN` on the system drive of every node. Rename folders
to meaningful names before placing data.

## I/O modes
- **Direct**: normal.
- **File system redirected**: per volume, for example when a backup application takes CSV snapshots or the CSV is
  manually placed in redirected mode.
- **Block redirected**: at file-block level, for example when storage connectivity is lost; faster than file system
  redirection.
CSVs formatted with ReFS on a SAN run in redirected I/O mode: format SAN volumes with NTFS and Storage Spaces Direct
volumes with ReFS.

## Balance and maintenance
```powershell
Move-ClusterSharedVolume -Name 'Cluster Disk 2' -Node NODE2
Suspend-ClusterResource 'Cluster Disk 2'    # maintenance mode for chkdsk etc.
Resume-ClusterResource 'Cluster Disk 2'
```
Since Windows Server 2012 R2, CSV ownership is distributed across nodes by the number of CSVs each owns and rebalanced
automatically on events such as failover.

## CSV in-memory read cache
```powershell
(Get-Cluster).BlockCacheSize = 2048      # MB reserved per node; suits read-intensive workloads such as VDI
```

## Troubleshoot
- Event 5120: interruption between a node and the CSV. The status code in the description names the cause (for example
  STATUS_BAD_NETWORK_PATH or STATUS_CONNECTION_DISCONNECTED, often SMB connectivity to the owner node).
- Event 5142: a non-owner node is disconnected and CSV is no longer queuing its I/O.
- When a CSV is in redirected mode, `Get-ClusterSharedVolumeState` shows the reason.

## Verify
- [ ] All CSVs Direct on every node (`StateInfo Direct`).

## Checked

Confirmed 2026-10-25 against the Windows Server docs (failover-cluster-csvs, failover-cluster-manage-cluster-shared-volumes, use-csv-cache and the CSV event 5120/5142 support articles; repository last commit 2026-10-23) and the Suspend-ClusterResource reference: redirected I/O modes, ReFS on SAN always redirected, ownership distribution since 2012 R2, BlockCacheSize and its read-intensive use, maintenance mode via Suspend-ClusterResource, events 5120 and 5142. Removed the unconfirmed fltmc and MPIO advice and the 2016 balancing claim.

Method: documentation only; no commands were run.
