---
id: computing-software.systems-network-administration.windows-server.add-servers-and-drives-to-s2d
name: add-servers-and-drives-to-s2d
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-spaces-direct, s2d, add-s2d-node, add-clusternode, optimize-storagepool]
level: advanced
status: docs-checked
description: "Scale out Storage Spaces Direct: validate and add a node, let drives join the pool, rebalance, and grow volumes or change resiliency afterwards."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/add-nodes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/manage-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/drive-symmetry-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding servers and drives to Storage Spaces Direct

## Add a server
1. Identical (or supported) hardware, same OS build and drivers/firmware, networking (RDMA, VLANs, DCB) configured
   like the existing nodes, joined to the domain.
2. Validate including the new node:
```powershell
Test-Cluster -Node N1,N2,N3,N4 -Include 'Storage Spaces Direct','Inventory','Network','System Configuration'
```
3. Add it:
```powershell
Add-ClusterNode -Name N4 -Cluster S2DCL01
```
   Eligible drives on N4 are claimed into the pool automatically, and Storage Spaces Direct optimizes drive usage after drives
   or servers are added.
4. Rebalance:
```powershell
Get-StoragePool S2D* | Optimize-StoragePool
Get-StorageJob
```

## Going from 2 or 3 nodes to more
- 2 servers: only two-way mirror. At 3 servers you can create three-way mirror volumes (pass the resiliency explicitly, or set
  `PhysicalDiskRedundancyDefault = 2` on the pool's Mirror ResiliencySetting); existing two-way volumes cannot be upgraded in
  place (create new volumes and copy the data).
- 4+ servers enable dual parity (set `PhysicalDiskRedundancy = 2` on the Parity ResiliencySetting to make it the default) and
  mirror-accelerated parity (create the Performance and Capacity tier templates first).
- With chassis or rack fault tolerance, create a temporary node fault domain and move it under its chassis or rack
  (`New-ClusterFaultDomain -Type Node`, `Set-ClusterFaultDomain -Parent`) before adding the server.

## Add drives to existing nodes
Add the same drives to every server (keep drive layout symmetric). They appear in `Get-PhysicalDisk` with `CanPool` = True and
are claimed automatically; if `CanPool` is False, `CannotPoolReason` says why (for example leftover partitions: clear them).
Usage is optimized automatically; `Optimize-StoragePool` runs it manually.

## Grow volumes
```powershell
Get-StorageTier <TierName> | Resize-StorageTier -Size 4TB   # volumes with storage tiers (find them with Get-VirtualDisk <name> | Get-StorageTier)
Get-VirtualDisk Vol02 | Resize-VirtualDisk -Size 4TB        # volumes without tiers
```
Then extend the partition with `Resize-Partition`.

## Verify
- [ ] `Get-StoragePool` shows new capacity; storage jobs complete; Health Service has no faults.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (add-nodes and manage-volumes; repository last commit 2026-10-23): validation with the Storage Spaces Direct category, Add-ClusterNode, automatic drive claiming and usage optimization, manual Optimize-StoragePool, two-way to three-way and dual parity upgrade rules and the PhysicalDiskRedundancyDefault and PhysicalDiskRedundancy settings, temporary node fault domain for chassis or rack awareness, CanPool and CannotPoolReason, Resize-VirtualDisk, Resize-StorageTier and Resize-Partition. Removed the unconfirmed FaultDomainAwarenessDefault claim and the second sources link (an Azure Local page not re-read this session).

Method: documentation only; no commands were run.
