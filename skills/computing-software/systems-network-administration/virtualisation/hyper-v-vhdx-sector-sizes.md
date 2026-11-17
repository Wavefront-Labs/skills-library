---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vhdx-sector-sizes
name: hyper-v-vhdx-sector-sizes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vhdx-sector-size, vhdx, hyper-v, storage]
level: advanced
status: docs-checked
description: "Choose VHDX logical and physical sector sizes (512e vs 4K native) and block size, check them in host and guest, and avoid application compatibility problems."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vhd
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/support-policy-4k-sector-hard-drives
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 4K sector sizes for VHDX

**Goal:** VHDX files aligned with modern 4K storage without breaking applications that expect 512-byte sectors.

## Two settings
- **Physical sector size**: valid values 512 and 4096.
- **Logical sector size**: valid values 512 and 4096. Logical 512 with physical 4096 is the 512e (Advanced Format) combination; 4096 and 4096 is 4K native (4Kn).
```powershell
New-VHD -Path "$vmPath\data.vhdx" -SizeBytes 500GB -Dynamic -LogicalSectorSizeBytes 4096 -PhysicalSectorSizeBytes 4096
Get-VHD "$vmPath\data.vhdx" | Select LogicalSectorSize, PhysicalSectorSize, BlockSize
Set-VHD -Path "$vmPath\data.vhdx" -PhysicalSectorSizeBytes 512    # physical can change; logical cannot
```
Inside a Windows guest, `fsutil fsinfo ntfsinfo <drive>:` reports Bytes Per Sector and Bytes Per Physical Sector (512/4096 is 512e, 4096/4096 is 4K native).

## Choosing
- Logical 512 (512e) is the most compatible choice when you are not sure.
- Some Windows features fail with logical sector drives other than 512 bytes (for example, system image backup and restore can fail); test applications and backup agents on 4K native disks first.
- Converting the logical sector size means a new VHDX and copying data in the guest; `Set-VHD` can change only the physical sector size.

## Block size
`New-VHD -BlockSizeBytes` sets the block size (the reference example uses 128 MB with a 4 KB logical sector size).

## Gotchas
- Windows supports 4K native drives from Windows 8 and Windows Server 2012 on; check application vendors for their own support statements.

## Verify
Host `Get-VHD` and guest tools both report the intended sizes.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: New-VHD -LogicalSectorSizeBytes and -PhysicalSectorSizeBytes accept 512 and 4096, -BlockSizeBytes, Set-VHD changes only -PhysicalSectorSizeBytes, 512e versus 4K native definitions, fsutil fsinfo ntfsinfo output fields, Windows support for 4K native from Windows 8 and Server 2012, and backup failures with non-512 logical sector drives. Removed as unconfirmed: the default sector sizes, default block size and the 1 MB Linux recommendation, SQL Server trace flag advice and application suitability list.

Method: documentation only; no commands were run.
