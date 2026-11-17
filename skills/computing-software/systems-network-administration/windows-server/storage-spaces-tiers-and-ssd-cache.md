---
id: computing-software.systems-network-administration.windows-server.storage-spaces-tiers-and-ssd-cache
name: storage-spaces-tiers-and-ssd-cache
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces, storage-pool, storage-tiers, new-storagetier, write-back-cache, ssd-cache, tiered-storage, optimize-volume, storage-tier-optimization]
level: advanced
status: docs-checked
description: "Build tiered standalone Storage Spaces: SSD and HDD tiers, write-back cache size, tier optimisation task, pinning files to the fast tier and checking tier usage."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/storage/new-storagetier
  - https://learn.microsoft.com/en-us/powershell/module/storage/new-virtualdisk
  - https://learn.microsoft.com/en-us/powershell/module/storage/set-filestoragetier
  - https://learn.microsoft.com/en-us/powershell/module/storage/optimize-volume
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-standalone-storage-spaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Spaces tiers and SSD write-back cache (standalone server)

Tiering places hot data on an SSD tier and cold data on an HDD tier inside one virtual disk. Placement changes
when tier optimization runs (`Optimize-Volume -TierOptimize`), so it suits workloads with a stable working set.

## Prerequisites
- Pool containing both SSD and HDD. Check `MediaType`; disks behind some HBAs report
  `Unspecified` and must be fixed first:
```powershell
Get-PhysicalDisk | Select FriendlyName,MediaType,Size,CanPool
Set-PhysicalDisk -FriendlyName 'PhysicalDisk3' -MediaType SSD
```
- Enough disks of each type for the tier's resiliency (a two-way mirror needs at least two disks).

## Create tiers and a tiered disk
```powershell
$ssd = New-StorageTier -StoragePoolFriendlyName Pool01 -FriendlyName SSDTier -MediaType SSD -ResiliencySettingName Mirror
$hdd = New-StorageTier -StoragePoolFriendlyName Pool01 -FriendlyName HDDTier -MediaType HDD -ResiliencySettingName Mirror
New-VirtualDisk -StoragePoolFriendlyName Pool01 -FriendlyName Tiered01 `
  -StorageTiers $ssd,$hdd -StorageTierSizes 400GB,8TB `
  -ResiliencySettingName Mirror -WriteCacheSize 1GB -ProvisioningType Fixed
```
- Spaces that use storage tiers must be **Fixed** provisioning (the `-ProvisioningType` documentation says so).
- `-WriteCacheSize` sets the write-back cache. If omitted, the pool's `WriteCacheSizeDefault` applies, which is
  Auto (Windows picks the size for your configuration); the pool default can be changed to a fixed value at any time.
  `-AutoWriteCacheSize` also exists.

## Tier optimisation
- Run tier optimization on demand (the cmdlet applies to tiered storage spaces with `-TierOptimize`):
```powershell
Optimize-Volume -DriveLetter E -TierOptimize -Verbose
```
Check the scheduled task and event logs on your own server for the optimization schedule and results; their
names and timing were not confirmed against documentation.

## Pin a file to SSD
```powershell
Set-FileStorageTier -FilePath '<vol>:\VMs\gold.vhdx' -DesiredStorageTierFriendlyName 'Tiered01-SSDTier'
Get-FileStorageTier -VolumeDriveLetter E   # Pinned vs placed status
```
The file must be on a volume hosted by the same tiered space. Pinning is also assigning a file to a tier; a file
already on a different tier moves the next time tier optimization runs. List tiers with `Get-StorageTier` to get the
exact tier name.

## Gotchas
- Tiered spaces cannot be thin provisioned; plan tier sizes up front.
- Resize each tier separately with `Resize-StorageTier`, then extend the partition with `Resize-Partition`.

## Verify
- [ ] `Get-StorageTier | Select FriendlyName,MediaType,Size` shows both tiers.
- [ ] `Get-VirtualDisk Tiered01 | Select WriteCacheSize,HealthStatus`.
- [ ] `Optimize-Volume -TierOptimize` completes without error.

## Checked

2026-10-27. Documentation release: Storage module cmdlet references for New-VirtualDisk, New-StorageTier, Set-FileStorageTier, Get-FileStorageTier, Optimize-Volume and Resize-StorageTier (Windows Server 2022 docset). Confirmed: Fixed required for tiers, WriteCacheSize default Auto and the pool default, -TierOptimize, pinning semantics, parameter names. Removed the 1 MB slab claim, the scheduled-task name and 01:00 time, the tiering event log name and counter wording, the 1 GB default cache, the cannot-change-later claim, the ReFS/NTFS pinning claim, the tier naming rule and the SSD-removal claim as unconfirmed.

Method: documentation only; no commands were run.
