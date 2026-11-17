---
id: computing-software.systems-network-administration.windows-server.storage-spaces-pools-and-virtual-disks
name: storage-spaces-pools-and-virtual-disks
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces, storage-pool, new-storagepool, new-virtualdisk, resiliency, mirror, parity, column-count, provisioning-type, storage-module]
level: practitioner
status: docs-checked
description: "Create standalone Storage Spaces: pool eligible disks, choose mirror vs parity and column count, fixed vs thin provisioning, then initialise and format the volume."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-standalone-storage-spaces
  - https://learn.microsoft.com/en-us/powershell/module/storage/new-virtualdisk
  - https://learn.microsoft.com/en-us/powershell/module/storage/new-storagepool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Spaces: pools and virtual disks (standalone server)

## Eligible disks
Pooling needs blank, unformatted disks of at least 4 GB with no volumes, on SAS or SATA, via simple HBAs or
RAID-capable HBAs in non-RAID mode (the adapter must not abstract or cache the disks). iSCSI and Fibre Channel are
supported only for nonresilient (Simple) spaces. Check why a disk is not poolable with `CannotPoolReason`.
```powershell
Get-PhysicalDisk | Format-Table FriendlyName,SerialNumber,MediaType,Size,BusType,CanPool,CannotPoolReason
```

## Create the pool
```powershell
$disks = Get-PhysicalDisk -CanPool $true
New-StoragePool -FriendlyName 'Pool01' -StorageSubSystemFriendlyName 'Windows Storage*' -PhysicalDisks $disks `
  -ResiliencySettingNameDefault Mirror -ProvisioningTypeDefault Fixed
```

## Virtual disk (space)
| Resiliency | Survives | Minimum disks | Good for |
|---|---|---|---|
| Simple | nothing | 1 | temporary or easily recreated data |
| Two-way mirror | 1 disk | 2 | most deployments, file shares, VHD libraries |
| Three-way mirror | 2 disks | 5 (hot spares not counted) | critical data |
| Parity | 1 disk | 3 | highly sequential archive or backup |
| Dual parity | 2 disks | see New-VirtualDisk | archive; needs Fixed provisioning |

Dual parity is `-ResiliencySettingName Parity -PhysicalDiskRedundancy 2` with `-ProvisioningType Fixed`. Three-way
mirror is `-NumberOfDataCopies 3` (or `-PhysicalDiskRedundancy 2`). Mirror uses dirty region tracking; parity uses
journaling to protect against unplanned shutdowns.

```powershell
New-VirtualDisk -StoragePoolFriendlyName 'Pool01' -FriendlyName 'Data01' `
  -ResiliencySettingName Mirror -NumberOfDataCopies 2 -NumberOfColumns 2 -Size 4TB -ProvisioningType Fixed
Get-VirtualDisk Data01 | Get-Disk | Initialize-Disk -PartitionStyle GPT -PassThru |
  New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume -FileSystem ReFS -NewFileSystemLabel Data01
```
- **Columns** (`-NumberOfColumns`, or `-AutoNumberOfColumns`) set how many disks each stripe spans; `Interleave`
  times columns is the size of one stripe of user data. See the New-VirtualDisk reference before choosing.
- **Fixed** provisioning allocates the full size from the pool at creation. **Thin** allocates on demand and can
  over-allocate, so monitor free pool space. Thin and fixed spaces can share a pool.
- A hot spare can be designated with `Add-PhysicalDisk -StoragePoolFriendlyName Pool01 -PhysicalDisks $d -Usage HotSpare`.

## Verify
- [ ] `Get-VirtualDisk | Select FriendlyName,ResiliencySettingName,NumberOfColumns,HealthStatus,OperationalStatus` = Healthy/OK.
- [ ] `Get-StoragePool Pool01 | Select Size,AllocatedSize` leaves repair headroom.

## Checked

2026-10-27. Documentation release: windowsserverdocs Deploy Storage Spaces on a stand-alone server (current) and the Storage module New-VirtualDisk and Set-PhysicalDisk references (Windows Server 2022 docset). Confirmed: disk and HBA requirements, iSCSI/FC limitation, minimum disks per resiliency type (2, 5, 3), New-StoragePool and New-VirtualDisk parameters including -PhysicalDiskRedundancy 2 and Fixed for dual parity, thin versus fixed behaviour, HotSpare usage. Removed the capacity-efficiency percentages, the 7-disk dual-parity figure, the 'add 4 disks' expansion rule and the spare-equals-largest-disk rule because no fetched page states them.

Method: documentation only; no commands were run.
