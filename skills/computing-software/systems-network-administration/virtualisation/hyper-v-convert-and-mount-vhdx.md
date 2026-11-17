---
id: computing-software.systems-network-administration.virtualisation.hyper-v-convert-and-mount-vhdx
name: hyper-v-convert-and-mount-vhdx
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [convert-vhd, mount-vhd, vhdx, dynamic-vhdx, offline-repair, hyper-v]
level: practitioner
status: docs-checked
description: "Convert VHD to VHDX and between fixed and dynamic with Convert-VHD, and mount VHDX files offline on the host for file recovery or repair without booting the VM."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/convert-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/mount-vhd
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convert and mount virtual disks

## Convert-VHD (VM off, writes a new file)
```powershell
Convert-VHD -Path "<VM_DIR>\old.vhd"  -DestinationPath "<VM_DIR>\old.vhdx" -VHDType Dynamic
Convert-VHD -Path "<VM_DIR>\db.vhdx"  -DestinationPath "<VM_DIR>\db-fixed.vhdx" -VHDType Fixed
Convert-VHD -Path x.vhdx -DestinationPath y.vhdx -VHDType Dynamic -BlockSizeBytes 1MB
```
Then repoint the VM: `Set-VMHardDiskDrive -VMName db -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 1 -Path <new>`.
Keep the old file until the VM boots from the new one. `-VHDType` accepts Fixed, Dynamic and Differencing, and `-DeleteSource` removes the source after conversion. For a differencing disk also give `-ParentPath`.

A generation 2 VM boots from VHDX (maximum boot volume 64 TB); a generation 1 boot volume is limited to 2 TB on VHDX and 2040 GB on VHD. A VHD to VHDX conversion does not change the partition style or make the disk UEFI-compatible: a generation cannot be changed after the VM is created.

## Mount offline
```powershell
Mount-VHD -Path "<VM_DIR>\app01.vhdx" -ReadOnly -Passthru | Get-Disk | Get-Partition | Get-Volume
# assign a letter if none
Get-Disk | ? Location -like "*app01.vhdx" | Get-Partition | ? Type -eq Basic | Add-PartitionAccessPath -AssignDriveLetter
Dismount-VHD -Path "<VM_DIR>\app01.vhdx"
```
Use cases: copy files out of a VM that won't boot or inspect logs. `Mount-VHD` also has `-NoDriveLetter` and `-SnapshotId`. Only mount disks of VMs that are off, and prefer `-ReadOnly`.

## Gotchas
- BitLocker-protected guest volumes need the recovery key; Linux file systems cannot be read by Windows: attach the disk to a Linux helper VM instead.

## Verify
New file attached and VM boots; `Get-VHD` shows expected VhdType; after mounting,
`Dismount-VHD` succeeds and the VM starts normally.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Convert-VHD and Mount-VHD references: -VHDType values, -BlockSizeBytes, -DeleteSource, -ParentPath, -ReadOnly, -Passthru, -NoDriveLetter and -SnapshotId; Dismount-VHD pairing. Confirmed in the generation page: generations cannot be changed, and the boot volume limits. Removed as unconfirmed: the performance table, the mbr2gpt remark, the running-VM, AVHDX and signature-collision gotchas, and the Linux block size recommendation.

Method: documentation only; no commands were run.
