---
id: computing-software.it-support-helpdesk.desktop-support.disk-management-and-diskpart
name: disk-management-and-diskpart
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-admin-tools, disk-management, diskpart, diskmgmt-msc, extend-volume, shrink-volume, drive-letter, initialize-disk, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Manage disks safely with Disk Management, diskpart and PowerShell: initialise, partition and format, extend/shrink volumes, drive letters, and fixing removable drives."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/storage/disk-management/overview-of-disk-management"
  - "https://learn.microsoft.com/en-us/windows-server/storage/disk-management/extend-a-basic-volume"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart"
  - "https://learn.microsoft.com/en-us/powershell/module/storage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# disk-management-and-diskpart

Goal: do disk tasks without wiping the wrong disk.

**Back up first.** Initialising, cleaning, formatting, shrinking and deleting
partitions can destroy data immediately. Confirm a current backup of anything
on the disk before any destructive step.

## Always identify first
```powershell
Get-Disk | Select Number, FriendlyName, SerialNumber, Size, PartitionStyle, BusType
Get-Volume | Select DriveLetter, FileSystemLabel, FileSystem, SizeRemaining, Size
```
Match size, bus type (USB vs NVMe) and serial before any destructive step.

## Common tasks
| Task | GUI (diskmgmt.msc) | PowerShell |
|---|---|---|
| New disk | Initialize (GPT), New Simple Volume | `Initialize-Disk 1 -PartitionStyle GPT; New-Partition 1 -UseMaximumSize -AssignDriveLetter \| Format-Volume -FileSystem NTFS -NewFileSystemLabel Data` |
| Extend a volume | Extend Volume (needs unallocated space **immediately after** it, on the same disk) | `Resize-Partition -DriveLetter C -Size (Get-PartitionSupportedSize -DriveLetter C).SizeMax` |
| Shrink | Shrink Volume | `Resize-Partition -DriveLetter D -Size 200GB` |
| Change letter | Change Drive Letter and Paths | `Set-Partition -DriveLetter E -NewDriveLetter S` |
| Mark online | Online | `Set-Disk 1 -IsOffline $false` |

## diskpart (WinRE, scripting)
```
diskpart
list disk
select disk 1
detail disk
list partition
clean          (destructive: wipes the disk's partition information)
convert gpt
create partition primary
format fs=ntfs quick label=Data
assign letter=E
```

## Typical support cases
- **Cannot extend C:** another partition (often the recovery partition) sits
  between C: and the free space, so Disk Management greys out Extend Volume.
  See the `gpt-uefi-partitioning-and-mbr2gpt` skill for moving the recovery
  partition.
- **USB stick shows the wrong size or will not format** after being an install
  stick: in diskpart select it, `clean`, then create a partition and format.
- **Drive has no letter**: assign one (new data disk, or a clash with a
  mapped drive).

## Gotchas
- `clean` on the wrong disk number destroys data at once; run `detail disk`
  and check the size and model first.

## Verify
`Get-Volume` shows the expected letters, sizes and file systems; data on
other disks is untouched.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Disk Management extend-a-volume, diskpart and Storage module cmdlet pages as published October 2026. Confirmed: unallocated space must be immediately after the volume on the same disk, Resize-Partition with Get-PartitionSupportedSize, Initialize-Disk, New-Partition, Format-Volume, Set-Partition and Set-Disk parameters used, diskpart clean and list disk. Removed: exam-objective reference, FAT32 and exFAT file-size notes, BitLocker-before-resize and dynamic-disk advice that no fetched page covers. Back-up-first warning added.

Method: documentation only; no commands were run.
