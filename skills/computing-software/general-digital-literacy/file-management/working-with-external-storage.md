---
id: computing-software.general-digital-literacy.file-management.working-with-external-storage
name: working-with-external-storage
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, usb-drive, flash-drive, sd-card, external-hard-drive, safely-eject, safely-remove-hardware, exfat, ntfs, fat32, apfs, formatting-a-drive, file-system, drive-letter, corrupted-usb, drive-not-detected, file-too-large-for-drive]
level: intro
status: draft
description: "Use USB drives, SD cards and external hard drives without corrupting files: safe ejection, choosing a file system, and what actually causes drive corruption."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with external storage — USB drives, SD cards and external disks without the corruption

**Goal:** move files to and from removable storage without losing them to the single
most common cause (pulling it out mid-write), and pick a file system that actually works
on every device you plan to use it with.

## 1. Safe ejection — the rule that prevents most corruption
Windows and macOS **cache writes in memory** before they're fully committed to the
drive, so a file can look "already copied" in the window while the drive is still
physically writing it in the background. Pulling the drive out at that moment is the
single biggest cause of corrupted drives and lost files.
- Windows: click the **Safely Remove Hardware** icon in the system tray (or right-click
  the drive in File Explorer › Eject) and wait for the "safe to remove" confirmation
  before pulling it.
- macOS: drag the drive icon to Trash (which becomes an eject arrow), or right-click ›
  **Eject**, and wait for it to disappear from the sidebar.
- A drive's **activity light still blinking** after you think a copy finished is a
  direct sign it's still writing — never pull it while that light is active.
- If Windows says "this device is in use" when ejecting: close any app that has a file
  open from that drive (including a stray File Explorer window still browsing it) and
  try again, rather than force-pulling it.

## 2. Choosing a file system when formatting
The file system determines which devices can read/write the drive and the single-file
size limit:
| File system | Works on | Max single file size | Notes |
|---|---|---|---|
| **exFAT** | Windows + macOS + most modern devices (cameras, game consoles) | effectively unlimited | Best general-purpose cross-platform choice today for a drive moved between Windows and Mac. |
| **FAT32** | Virtually everything, including very old devices | 4GB per file | Choose only for compatibility with an old device (some car stereos, older TVs); the 4GB file cap bites on any single large video. |
| **NTFS** | Windows natively; macOS can only **read**, not write, NTFS drives without extra software | effectively unlimited | Fine for a Windows-only external drive; a problem the moment a Mac needs to write to it. |
| **APFS/HFS+** | macOS; Windows cannot read either without extra software | effectively unlimited | Fine for a Mac-only drive; avoid if the drive will ever touch a Windows PC. |
- Format: Windows — right-click the drive in File Explorer › Format, choose the file
  system; macOS — Disk Utility › select the drive › Erase, choose the format.
  **Formatting erases everything on the drive** — back up first.
- A brand-new drive usually arrives pre-formatted exFAT or FAT32 specifically for
  cross-platform compatibility; reformatting is only needed if you have a specific
  reason (an old device, or converting from NTFS for Mac use).

## 3. "The drive isn't showing up" / drive letter issues
- Windows assigns a **drive letter** on connection; if another device already claims
  that letter, the drive can connect without appearing in File Explorer. Check Disk
  Management (right-click Start › Disk Management) — if the drive shows there but has
  no letter, right-click it › Change Drive Letter and Paths › Add, to assign one.
- A drive that shows in Disk Management as **"Unallocated"** has no usable file system
  on it from this computer's point of view — it needs formatting (section 2) before use,
  which is also the state a drive can end up in after a failed/interrupted format.
- Try a **different port and a different cable** (if the drive uses one) before
  concluding the drive itself has failed — see
  basic-troubleshooting.hardware-and-peripheral-troubleshooting for the general swap-one-
  thing-at-a-time method.

## 4. Why "corrupted" drives happen, and what that actually means
- Removing a drive mid-write (section 1) is the leading cause and typically corrupts
  the **file system's index**, not necessarily every file — a `chkdsk` (Windows: right-
  click drive › Properties › Tools › Error checking, or `chkdsk X: /f` in Command
  Prompt) or **First Aid** (macOS Disk Utility) can often repair the index and recover
  most files.
- A drive that corrupts **repeatedly** despite safe ejection is usually a hardware fault
  (failing flash memory, a dying USB controller) — stop trusting it for anything
  important rather than reformatting it again and hoping.
- USB sticks and SD cards have a **limited write-cycle lifespan** and are not a backup
  medium for anything irreplaceable long-term; treat them as transport, not storage —
  see organising-files-and-folders, section 6, for the 3-2-1 backup rule.

## Verify
- [ ] You wait for "safe to remove"/the eject confirmation before pulling any external drive.
- [ ] A drive used between Windows and Mac is formatted exFAT, not NTFS or APFS/HFS+.
- [ ] You know how to check Disk Management/Disk Utility when a connected drive doesn't
      show up as a normal folder.
- [ ] Anything irreplaceable also exists somewhere other than a single USB stick or SD card.
