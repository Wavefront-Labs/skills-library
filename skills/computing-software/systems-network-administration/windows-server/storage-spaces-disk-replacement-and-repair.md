---
id: computing-software.systems-network-administration.windows-server.storage-spaces-disk-replacement-and-repair
name: storage-spaces-disk-replacement-and-repair
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces, storage-pool, repair-virtualdisk, retire-physicaldisk, remove-physicaldisk, degraded, lost-communication, optimize-storagepool, pool-rebalance]
level: practitioner
status: docs-checked
description: "Replace a failed disk in a Storage Spaces pool: identify by serial, retire, add the new disk, repair virtual disks, watch storage jobs, remove the old disk, rebalance."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-states
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/replace-drives
  - https://learn.microsoft.com/en-us/powershell/module/storage/repair-virtualdisk
  - https://learn.microsoft.com/en-us/powershell/module/storage/set-physicaldisk
  - https://learn.microsoft.com/en-us/powershell/module/storage/remove-physicaldisk
  - https://learn.microsoft.com/en-us/powershell/module/storage/optimize-storagepool
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Storage Spaces disk replacement and repair

## 1. Identify
```powershell
Get-PhysicalDisk | ? HealthStatus -ne 'Healthy' | Select FriendlyName,SerialNumber,HealthStatus,OperationalStatus,Usage,PhysicalLocation
Get-VirtualDisk | Select FriendlyName,HealthStatus,OperationalStatus
```
Drive operational states include Lost communication (drive missing; health Warning), Predictive failure (replace
the drive), IO error and Transient error (try `Reset-PhysicalDisk` then `Repair-VirtualDisk`; replace if it recurs),
Failed media and Device hardware failure (replace). Virtual disks show `Incomplete` (missing drives still hold
current data) or `Degraded` (outdated copies) while resilience is reduced; for non-S2D pools run `Repair-VirtualDisk`
after reconnecting or replacing drives. Match the **serial number** to the physical slot
(`Enable-PhysicalDiskIdentification -FriendlyName ...`, where the enclosure supports it).

## 2. Retire the failing disk (if still present)
```powershell
$bad = Get-PhysicalDisk -SerialNumber '<SERIAL>'
Set-PhysicalDisk -InputObject $bad -Usage Retired
Get-VirtualDisk | Repair-VirtualDisk -AsJob      # rebuild data onto remaining disks/new disk
Get-StorageJob                                   # progress; wait for completion
```

## 3. Add the replacement
```powershell
$new = Get-PhysicalDisk -CanPool $true
Add-PhysicalDisk -StoragePoolFriendlyName 'Pool01' -PhysicalDisks $new
Get-VirtualDisk | Repair-VirtualDisk -AsJob
```

## 4. Remove the old disk from the pool
Only after all virtual disks are Healthy:
```powershell
Remove-PhysicalDisk -StoragePoolFriendlyName 'Pool01' -PhysicalDisks $bad
```
Then physically pull it.

## 5. Rebalance
```powershell
Optimize-StoragePool -FriendlyName 'Pool01'     # rebalances allocations onto disks with available capacity
```
A pool state of Suboptimal (data not written evenly across drives) is the documented cue to run it.

## Gotchas
- Never remove a disk while virtual disks are Degraded: you may drop below redundancy.
- Lost communication can mean a missing or disconnected drive rather than a failed one; reconnect and recheck
  before replacing.
- On Storage Spaces Direct, failed drives are retired and evacuated automatically and a repair starts on its own;
  follow the S2D replace-drives procedure instead.

## Verify
- [ ] All `Get-VirtualDisk` Healthy/OK; no `Get-StorageJob` running.
- [ ] Old disk absent from `Get-PhysicalDisk -StoragePool (Get-StoragePool Pool01)`.

## Checked

2026-10-27. Documentation release: windowsserverdocs Storage Spaces health and operational states (current), Replace drives in Storage Spaces Direct, and the Storage module references for Set-PhysicalDisk (Usage Retired), Remove-PhysicalDisk, Optimize-StoragePool and Enable-PhysicalDiskIdentification (Windows Server 2022 docset). Confirmed state names and actions, parameter names and the Retired usage value. Removed the headroom-equals-one-disk rule as unconfirmed.

Method: documentation only; no commands were run.
