---
id: computing-software.systems-network-administration.windows-server.s2d-enable-and-cache-configuration
name: s2d-enable-and-cache-configuration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces-direct, s2d, enable-clusters2d, failover-clustering, test-cluster, s2d-cache, cache-devices, hyperconverged]
level: advanced
status: docs-checked
description: "Enable Storage Spaces Direct on a validated cluster: clean drives, Test-Cluster with S2D tests, Enable-ClusterS2D, cache binding and media-type checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-storage-spaces-direct
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/cache
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-direct-hardware-requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable Storage Spaces Direct and configure the cache

## Before enabling
- 2 to 16 servers, Datacenter edition, drives directly attached to one server each (HBA or pass-through only, no RAID or
  SAN), at least 10 Gbps networking with RDMA recommended (iWARP, or RoCE with correctly configured switches and DCB).
- Wipe every non-boot drive on every node; old pool metadata blocks pooling:
```powershell
Invoke-Command $nodes {
  Get-StoragePool | ? IsPrimordial -eq $false | Set-StoragePool -IsReadOnly $false -EA 0
  Get-StoragePool | ? IsPrimordial -eq $false | Remove-StoragePool -Confirm:$false -EA 0
  Get-Disk | ? { -not $_.IsBoot -and -not $_.IsSystem -and $_.PartitionStyle -ne 'RAW' } | % {
    $_ | Set-Disk -IsOffline:$false; $_ | Set-Disk -IsReadOnly:$false
    $_ | Clear-Disk -RemoveData -RemoveOEM -Confirm:$false }
}
```

## Validate and create
```powershell
Test-Cluster -Node $nodes -Include 'Storage Spaces Direct','Inventory','Network','System Configuration'
New-Cluster -Name S2DCL01 -Node $nodes -NoStorage -StaticAddress 10.0.0.50
Set-ClusterQuorum -CloudWitness -AccountName <storageacct> -AccessKey <key>
Enable-ClusterS2D -Verbose
```
- `-NoStorage` is mandatory: never let New-Cluster claim the disks.
- Enable-ClusterS2D creates one pool (`S2D on <cluster>`), enables the fastest media as cache when several media types
  are present, and creates default Capacity and Performance tiers.

## Cache behaviour
| Drives present | Cache device | Cache role |
|---|---|---|
| NVMe + SSD | NVMe | write-only |
| NVMe or SSD + HDD | fastest | read and write for HDD |
| All NVMe or all SSD | none by default (optional, configure manually) | write-only if configured |
- At least two cache drives per server so a cache failure does not leave all bound capacity drives unprotected; cache
  devices must be 32 GB or larger, and capacity drives should be a whole multiple of the cache drives.
- Binding is dynamic: capacity drives rebind to surviving cache devices.
- All-flash read/write caching: `Set-ClusterStorageSpacesDirect -CacheModeSSD ReadWrite`.
- Check eligibility with `Get-PhysicalDisk | Select FriendlyName,BusType,MediaType,CanPool,CannotPoolReason`.

## Verify
- [ ] `Get-ClusterStorageSpacesDirect` shows the expected CacheModeHDD/CacheModeSSD.
- [ ] `Get-PhysicalDisk | Group Usage` shows the cache and capacity drives.
- [ ] `Get-HealthFault` returns nothing.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (deploy-storage-spaces-direct, cache, storage-spaces-direct-overview and hardware requirements; repository last commit 2026-10-23): 2 to 16 servers, Datacenter edition, at least 10 Gbps networking with RDMA recommended (iWARP or RoCE), validation command with the Storage Spaces Direct category, New-Cluster -NoStorage, Enable-ClusterStorageSpacesDirect (alias Enable-ClusterS2D) behaviour, the default cache behaviour table, dynamic cache binding, two cache drives per server minimum, 32 GB cache minimum, Set-ClusterStorageSpacesDirect -CacheModeSSD ReadWrite. Removed the unconfirmed 10 percent cache sizing rule and the CacheState and Journal usage checks.

Method: documentation only; no commands were run.
