---
id: computing-software.systems-network-administration.windows-server.extend-storage-spaces-virtual-disks
name: extend-storage-spaces-virtual-disks
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-spaces, resize-virtualdisk, resize-partition, storage-pool, thin-provisioning]
level: practitioner
status: docs-checked
description: "Grow Storage Spaces capacity: add disks to the pool, Resize-VirtualDisk, then extend the partition and volume."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/storage/resize-virtualdisk
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/manage-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-standalone-storage-spaces
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Extending Storage Spaces virtual disks

## 1. Add capacity to the pool
```powershell
Get-PhysicalDisk -CanPool $true
Add-PhysicalDisk -StoragePoolFriendlyName Pool01 -PhysicalDisks (Get-PhysicalDisk -CanPool $true)
```

## 2. Know the column constraint
A virtual disk stripes one stripe of data across `NumberOfColumns` physical disks. Check the layout and the pool's free
space before growing; if the pool cannot place the extra space, the resize fails.
```powershell
Get-VirtualDisk Data01 | Select FriendlyName,ResiliencySettingName,NumberOfColumns,NumberOfDataCopies,Size,FootprintOnPool
Get-StoragePool Pool01 | Select Size,AllocatedSize
```
After adding disks, `Optimize-StoragePool Pool01` rebalances the Spaces allocations onto disks with available capacity; it is
I/O intensive.

## 3. Resize the virtual disk
```powershell
Resize-VirtualDisk -FriendlyName Data01 -Size 8TB
# tiered disks: resize the tiers instead
Get-VirtualDisk Data01 | Get-StorageTier | Resize-StorageTier -Size 6TB
```

## 4. Extend the partition and volume
```powershell
$part = Get-VirtualDisk Data01 | Get-Disk | Get-Partition | Where-Object Type -eq 'Basic'
$max = ($part | Get-PartitionSupportedSize).SizeMax
$part | Resize-Partition -Size $max
```
Cluster Shared Volumes: run on the coordinator node.

## Gotchas
- Whether a virtual disk can expand or shrink is vendor specific (Resize-VirtualDisk); plan sizes.
- Thin-provisioned disks can over-allocate the pool: monitor the pool's AllocatedSize.

## Verify
- [ ] `Get-Volume` shows the new size; pool and virtual disk health OK.

## Checked

Confirmed 2026-10-25 against the Windows Server 2025 PowerShell reference (Resize-VirtualDisk note that expanding or shrinking is vendor specific, New-VirtualDisk NumberOfColumns, Optimize-StoragePool rebalancing and I/O cost) and the Windows Server docs (manage-volumes for Resize-VirtualDisk, Resize-StorageTier and the Resize-Partition steps, and deploy-standalone-storage-spaces for thin provisioning and Add-PhysicalDisk). Removed the unconfirmed column free-space rule and its example, the online NTFS/ReFS claim, the shrinking claim, the 70-80 percent alert level and the parity growth claim.

Method: documentation only; no commands were run.
