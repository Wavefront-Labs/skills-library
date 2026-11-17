---
id: computing-software.general-digital-literacy.basic-troubleshooting.backup-and-system-recovery
name: backup-and-system-recovery
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, backup, system-restore, time-machine, recovery-drive, factory-reset, reset-this-pc, reinstall-windows, macos-recovery, restore-point]
level: intro
status: docs-checked
description: "Set up Windows Backup and Time Machine before trouble, then pick the least disruptive recovery: troubleshooter, uninstall an update, restore, reset or reinstall."
sources:
  - https://support.microsoft.com/en-us/windows/experience/backup-recovery/recovery-options-in-windows
  - https://support.apple.com/guide/mac-help/back-up-files-mh35860/mac
  - https://support.apple.com/guide/mac-help/reinstall-macos-mchlp1599/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and system recovery

**Goal:** have a copy of your data and a recovery route set up before anything goes wrong, and choose the least disruptive recovery option. Some recovery options can lose data, so **back up your important files before you start**.

## Set up before you need it
- **Windows:** turn on **Windows Backup** (Settings > Accounts > Windows Backup) to save apps and settings so they can be restored after a recovery. Know your **BitLocker recovery key** if BitLocker is on; most WinRE recovery options need it. Create a **recovery drive** while the PC works: search for *Recovery Drive*, keep *Back up system files to the recovery drive* ticked, and use an empty USB drive (it is erased).
- **Mac:** use **Time Machine**. Connect an external disk, then Time Machine menu bar icon > Open Time Machine Settings > **Add Backup Disk** (to show the icon: System Settings > Control Center > Time Machine > Show in Menu Bar). Time Machine makes hourly, daily and weekly backups, and also keeps local snapshots for up to 24 hours or until space is needed on APFS disks. Apple recommends a backup on a separate disk or network location, not the internal disk. It does not back up system files or apps installed with macOS. A backup made on macOS 12 or later can only be restored to a Mac running macOS 11 or later.

## Windows recovery options (Microsoft: try them in this order if the PC starts)
1. **Troubleshooter:** Settings > System > Troubleshoot > Other troubleshooters.
2. **Reinstall Windows** (Windows 11 22H2 or later): reinstalls the current version without affecting files, apps or settings.
3. **Uninstall a Windows update**: files and apps are not affected. If the problem began after upgrading to a new Windows version, go back to the previous one (available for 10 days after upgrading).
4. **Point-in-time restore** (Windows 11 24H2 or later): rolls back the whole PC including apps, settings and personal files to a recent automatic restore point; restore points are kept for up to 3 days. Files in OneDrive or other cloud storage are not affected.
5. **Reset this PC**: reinstalls Windows from scratch; you choose to keep your personal files or remove everything; apps and settings are removed. The most disruptive of these.
- **System Restore** rolls back system files and settings but not personal files; use it if point-in-time restore is unavailable or you need a restore point older than 3 days.
- If the PC will not start, use WinRE options: Point-in-time restore, Uninstall updates (Troubleshoot > Advanced options), Reset this PC (Troubleshoot > Reset this PC), or reinstall from recovery media. Recovery media from the PC maker may include hardware drivers that generic Microsoft media does not.
- Reinstall from installation media or a recovery drive removes your personal files, apps and settings, so back up first. For suspected malware, run a Windows Security scan first; if the problem continues, a clean installation removes everything on the selected drive.

## Mac recovery
**macOS Recovery** keeps your files and user settings when it reinstalls macOS (internet connection required). Apple silicon: Apple menu > Shut Down, then hold the power button until startup options appear, choose Options. Intel: restart and hold Command-R (reinstall current version), Option-Command-R (latest compatible) or Option-Shift-Command-R (original version). Choose **Reinstall macOS** and select your current volume. Before you sell or trade in a Mac, use Erase Assistant (Apple silicon or T2 Macs) instead.

## Disk health
If the drive shows errors, back up immediately. On Windows, `chkdsk /f C:` in an administrator Command Prompt starts repairs and asks you to restart. On a Mac, Disk Utility can repair a startup disk from Recovery.

## Verify
- [ ] Windows Backup or Time Machine is turned on now, and you know where your BitLocker key and recovery drive are.

## Checked
Checked 2026-10-27 against Microsoft Support "Recovery options in Windows" and "Troubleshoot problems updating Windows" (chkdsk step), and the Apple Mac User Guide pages "Back up your files with Time Machine on Mac" and "Reinstall macOS", plus Apple Support 102535 (Disk Utility repair from Recovery). Confirmed: backup and recovery drive steps, the five-option order and what each keeps or removes, 10-day and 3-day limits, WinRE paths, Time Machine behaviour and limits, Recovery key combinations and data kept, Erase Assistant. Removed unconfirmed claims (System Protection and Create a restore point dialog steps, File History path, 16 GB recovery drive size, drive failure signs, SMART tools, Erase All Content and Settings menu path).
Method: documentation only; no commands were run.
