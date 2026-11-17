---
id: computing-software.it-support-helpdesk.desktop-support.gpt-uefi-partitioning-and-mbr2gpt
name: gpt-uefi-partitioning-and-mbr2gpt
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, gpt-uefi, mbr, mbr2gpt, efi-system-partition, msr, recovery-partition, csm, legacy-bios, diskpart, windows-installation, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Choose GPT/UEFI vs MBR/legacy, read a disk's partition layout, convert MBR to GPT in place with MBR2GPT, and fix the recovery partition after resizing."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions"
  - "https://learn.microsoft.com/en-us/windows/deployment/mbr-to-gpt"
  - "https://support.microsoft.com/en-us/servicing/os/windows/2023/06/kb5028997-instructions-to-manually-resize-your-partition-to-install-the-winre-update"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/windows-boot-issues-troubleshooting"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gpt-uefi-partitioning-and-mbr2gpt

Goal: get every PC onto GPT plus UEFI (a Windows 11 prerequisite) and
understand the partition layout well enough to fix it.

**Back up first.** Disk conversion and partition deletion can leave a PC
unbootable or lose data. Take a full backup and keep the BitLocker recovery
key before you start.

## Know what you have
```powershell
Get-Disk | Select Number, FriendlyName, PartitionStyle, Size
Get-Partition -DiskNumber 0 | Select PartitionNumber, Type, Size, DriveLetter
```
Boot loader file: `winload.exe` is the BIOS path and `winload.efi` the UEFI
path in Microsoft's boot sequence table.

## Microsoft's UEFI/GPT layout
1. EFI System Partition (ESP), FAT32, minimum 200 MB on 512-byte-sector
   drives, 300 MB on 4K-native drives. It should hold no other files.
2. Microsoft reserved partition (MSR), 16 MB.
3. Windows partition (NTFS), at least 20 GB for 64-bit.
4. Recovery partition (WinRE), Type ID `DE94BBA4-06D1-4D40-A16A-BFD50179D6AC`,
   separate from the Windows partition and placed **immediately after** it.
   Size = winre.wim plus customisations plus 250 MB free for servicing
   (recommended minimum for a custom script is 990 MB with 250 MB free).

## Converting in place
```cmd
mbr2gpt /validate /disk:0 /allowFullOS
mbr2gpt /convert  /disk:0 /allowFullOS
```
Validation requires: the disk is MBR, room for the GPTs (16 KB plus 2 sectors
at the front, 16 KB plus 1 sector at the end), at most three primary
partitions, no extended or logical partitions, an active system partition, a
BCD default OS entry that points to an OS partition, and recognised partition
types. It converts system disks only, and without deleting data.
BitLocker: suspend protection first; afterwards the existing protectors must
be deleted and recreated to resume. **After conversion the firmware must be
reconfigured to boot in UEFI mode**; confirm the device supports UEFI first.
Logs: `setupact.log`, `setuperr.log`, `diagerr.xml`, `diagwrn.xml`, default
location `%windir%` in Windows PE (use `/logs` to choose).

## Recovery partition too small for the WinRE update
Microsoft's KB5028997: a system event 4502 "Windows Recovery Environment
servicing failed" (ErrorPhase 2) usually means the recovery partition is too
small. The documented fix (requires the recovery partition after the OS
partition) is to grow it by 250 MB:
```cmd
reagentc /info
reagentc /disable
diskpart
  list disk
  sel disk <OS disk index>
  list part
  sel part <OS partition index>
  shrink desired=250 minimum=250
  sel part <WinRE partition index>
  delete partition override
  create partition primary id=de94bba4-06d1-4d40-a16a-bfd50179d6ac
  gpt attributes =0x8000000000000001
  format quick fs=ntfs label="Windows RE tools"
  exit
reagentc /enable
reagentc /info
```
That is the GPT procedure. For an MBR disk the KB uses `create partition
primary id=27` and `set id=27`. Check the disk and partition numbers twice;
`delete partition override` destroys the partition you select. If creation
fails, run `reagentc /enable` to restore WinRE.

## Verify
`Get-Disk 0` shows GPT, the firmware boots in UEFI mode, and `reagentc /info`
shows Windows RE enabled.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn UEFI/GPT partition configuration, MBR2GPT and Windows boot troubleshooting pages, and Microsoft Support KB5028997, as published October 2026. Confirmed: ESP 200/300 MB minimums, MSR 16 MB, recovery partition type ID, placement, size formula and 990 MB/250 MB figures, every MBR2GPT validation prerequisite, BitLocker suspend and protector recreation, UEFI reconfiguration warning, log names and WinPE default location, winload.exe/winload.efi, and the full KB5028997 diskpart procedure including GPT and MBR variants. Removed: ESP 100 MB figure, 750 MB recovery size, 2 TB and four-primary MBR limits, the 1703 version gate, mbr2gpt Cannot find OS partition tip, dual-boot and third-party encryption notes, KB5034441 error code.

Method: documentation only; no commands were run.
