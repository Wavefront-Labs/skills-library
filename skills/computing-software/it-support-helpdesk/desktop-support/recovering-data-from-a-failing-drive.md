---
id: computing-software.it-support-helpdesk.desktop-support.recovering-data-from-a-failing-drive
name: recovering-data-from-a-failing-drive
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, backup, data-recovery, failing-drive-recovery, ddrescue, smart, bad-sectors, clicking-drive, data-recovery-service, bitlocker-unlock, usb-enclosure]
level: advanced
status: draft
description: "Rescue data from a dying HDD or SSD: stop writing, read SMART, image first with ddrescue, unlock BitLocker on the copy, and know when to stop and send it to a recovery lab."
sources:
  - "https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde-unlock"
  - "https://www.smartmontools.org/wiki/TocDoc"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# recovering-data-from-a-failing-drive

Goal: get the data off before the drive dies completely, and never make it
worse.

## First, is it worth the risk?
- Is the data elsewhere (OneDrive, server, backup)? Most managed users' data
  is — confirm before heroics.
- **Physical symptoms** (clicking, grinding, beeping, not spinning, drive
  dropped, burnt smell): power it off and send to a professional recovery
  lab. Every power-on can scrape platters. Don't open it, don't freeze it.

## Logical/degrading drive (still detected, slow, read errors)
1. Stop using it: no chkdsk, no defrag, no booting Windows from it (Windows
   writes on boot, chkdsk "fixes" by discarding data).
2. Check SMART from another machine (USB enclosure/dock):
   `smartctl -a /dev/sdX` — Reallocated_Sector_Ct, Current_Pending_Sector,
   Offline_Uncorrectable rising = media failing. NVMe: `smartctl -a
   /dev/nvme0` → Percentage Used, Media and Data Integrity Errors.
3. **Image first**, recover from the image:
   ```bash
   ddrescue -n /dev/sdX disk.img disk.map       # fast pass, skip bad areas
   ddrescue -d -r3 /dev/sdX disk.img disk.map   # retry bad areas, direct I/O
   ```
   Destination needs more free space than the source size. The map file
   lets you resume.
4. Mount/open the image (read-only) and copy files out; for corrupted
   filesystems use TestDisk/PhotoRec against the image, not the drive.

## BitLocker drives
You need the recovery key. Unlock the clone/image (attached as a disk) in
Windows: `manage-bde -unlock E: -RecoveryPassword <48-digit key>`, or
`dislocker` on Linux. Without the key, the data is unrecoverable by
design.

## SSD specifics
SSDs often fail suddenly (controller) and go read-only or vanish; TRIM
makes deleted-file recovery near impossible. If it's detected in read-only
mode, copy immediately. Firmware-failed SSDs need a lab.

## Gotchas
- Imaging tools on Windows (some "clone" tools) give up on read errors —
  use ddrescue (Linux live USB) for failing media.
- Chain of custody and data protection still apply — recovery labs need a
  contract/NDA; log the handover.
- Don't promise success; set expectations in writing.

## Verify
Recovered files open (spot-check documents of each type), user confirms
critical items, failing drive is logged for sanitisation/destruction.
