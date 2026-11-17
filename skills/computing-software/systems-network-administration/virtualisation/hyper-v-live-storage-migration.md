---
id: computing-software.systems-network-administration.virtualisation.hyper-v-live-storage-migration
name: hyper-v-live-storage-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, move-vmstorage, storage-migration, live-storage-migration, vhdx, csv, windows-server]
level: practitioner
status: docs-checked
description: "Move a running Hyper-V VM's VHDX and configuration files to new storage with Move-VMStorage, including per-disk destinations, concurrency and cleanup checks."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/move-vmstorage
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/live-migration-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live storage migration on Hyper-V

**Goal:** relocate a VM's disks (new LUN, CSV rebalance, array retirement) with no guest downtime.

## Move everything to one folder
```powershell
Move-VMStorage -VMName app01 -DestinationStoragePath '<CSV_ROOT>\Volume2\app01'
```

## Move disks individually
```powershell
Move-VMStorage -VMName app01 `
  -VirtualMachinePath '<CSV_ROOT>\Volume2\app01' `
  -SnapshotFilePath   '<CSV_ROOT>\Volume2\app01' `
  -SmartPagingFilePath '<CSV_ROOT>\Volume2\app01' `
  -VHDs @(@{SourceFilePath='<CSV_ROOT>\Volume1\app01\data.vhdx';
            DestinationFilePath='<CSV_ROOT>\Volume3\app01\data.vhdx'})
```

## Concurrency
```powershell
Set-VMHost -MaximumStorageMigrations 2
```

## Gotchas
- The destination needs free space for all disks plus checkpoints.
- `-RetainVhdCopiesOnSource` keeps the source copies, and `-RemoveSourceUnmanagedVhds` removes source files not attached to the VM; decide before you run it.

## Verify
`Get-VMHardDiskDrive -VMName app01 | Select-Object Path` shows the new paths, the source folder is empty, and `Get-VM app01 | Select-Object Path, ConfigurationLocation` updated.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Move-VMStorage reference: -DestinationStoragePath, -VirtualMachinePath, -SnapshotFilePath, -SmartPagingFilePath, -Vhds (hashtable list with SourceFilePath and DestinationFilePath), -RetainVhdCopiesOnSource, -RemoveSourceUnmanagedVhds and Set-VMHost -MaximumStorageMigrations. Removed as unconfirmed: the mirroring explanation, the cluster behaviour, the Resilient Change Tracking effect and the shared disk and pass-through limits.

Method: documentation only; no commands were run.
