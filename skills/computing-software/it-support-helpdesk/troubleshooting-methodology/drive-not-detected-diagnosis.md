---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.drive-not-detected-diagnosis
name: drive-not-detected-diagnosis
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, storage-troubleshooting, drive-not-detected, nvme-not-detected, bios-storage, vmd, raid-mode, uninitialized-disk, no-boot-device, comptia-a-plus, boot-device-not-found]
level: practitioner
status: draft
description: "Find why a drive isn't seen: firmware detection, SATA/NVMe mode and VMD, cabling and M.2 slot compatibility, uninitialised or offline disks in Disk Management, and dead drives."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://learn.microsoft.com/en-us/windows-server/storage/disk-management/troubleshooting-disk-management"
  - "https://www.smartmontools.org/wiki/TocDoc"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# drive-not-detected-diagnosis

Goal: locate the layer where a missing drive disappears — firmware,
controller mode, OS, or the drive itself (A+ 220-1201 5.3).

## Layer 1: does the firmware see it?
Enter BIOS/UEFI setup → storage/NVMe/SATA information.
- **Not listed**: power/data connection, slot compatibility, or dead drive.
  - SATA: reseat both cables, swap data cable and port, check PSU connector.
  - M.2: correct key (M vs B+M), NVMe vs SATA support in that slot, screw
    seated, some boards disable a SATA port when an M.2 slot is in use
    (manual's lane-sharing table).
  - Try the drive in a USB enclosure on another PC — still nothing = dead.
- **Listed** → continue.

## Layer 2: controller mode
- **Intel VMD / RST (RAID On)**: Windows setup and some tools can't see NVMe
  behind VMD without the driver; Linux live USBs often can't either. Load
  the VMD driver in setup, or switch to AHCI only for wipe-and-reinstall
  (switching on an installed OS = INACCESSIBLE_BOOT_DEVICE).
- Legacy/CSM boot can't boot NVMe on many boards — UEFI only.

## Layer 3: Windows sees hardware, not volume
Disk Management (`diskmgmt.msc`) / `Get-Disk`:
| State | Action |
|---|---|
| **Not Initialized** (new drive) | Initialize (GPT), create volume — never on a disk with data you need |
| **Offline** (policy/signature collision) | right-click → Online; `Set-Disk -Number 1 -IsOffline $false` |
| **Unallocated** | create volume (new) or recovery (if it had data) |
| **RAW** filesystem | filesystem damaged — data recovery, don't format |
| No drive letter | assign one |
| Foreign (dynamic disk) | Import Foreign Disks |
Device Manager → Disk drives / Storage controllers: yellow bang = driver.

## Layer 4: no boot device
"No bootable device" but drive listed: boot order, missing EFI entry
(`bcdboot` repair), or drive wiped. Check the drive's partitions from
WinRE/live USB.

## Gotchas
- Initialising or formatting to "make it show up" destroys data — confirm
  it's empty first.
- Drives over 2 TB on MBR show only 2 TB; use GPT.
- Some external drives need more USB power — use a powered hub / Y-cable.

## Verify
Drive visible in firmware, Disk Management shows Online/Healthy with the
expected capacity, and data (if any) is readable.
