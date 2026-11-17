---
id: computing-software.it-support-helpdesk.desktop-support.macos-time-machine-migration-and-activity-monitor
name: macos-time-machine-migration-and-activity-monitor
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, time-machine-backup, migration-assistant, activity-monitor, macos, backup, mac-performance]
level: practitioner
status: draft
description: "Support Mac users with Time Machine backups and restores, Migration Assistant moves to a new Mac, and Activity Monitor triage of slow or hot machines."
sources:
  - "https://support.apple.com/en-us/104984"
  - "https://support.apple.com/en-us/102613"
  - "https://support.apple.com/guide/activity-monitor/welcome/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-time-machine-migration-and-activity-monitor

## Time Machine
- Set up: System Settings > General > Time Machine > Add Backup Disk (local APFS disk, or
  SMB share from a NAS that advertises Time Machine support). Encrypt the backup.
- Hourly snapshots for 24 h, daily for a month, weekly until full.
- Check status: `tmutil status`, `tmutil latestbackup`, `tmutil listbackups`;
  exclusions: `tmutil isexcluded <path>`.
- Restore a file: open the folder in Finder, click Time Machine in the menu bar >
  Browse Time Machine backups, pick the date, Restore.
- Full restore: Recovery > Restore from Time Machine (to the same or a replacement Mac).
- Corporate note: Time Machine is a personal-device safety net; corporate data should
  live in OneDrive/SharePoint or a managed backup. MDM can block or require Time Machine
  and set the destination.
- Problems: "Backup disk not available" (network share sleeping, credentials changed),
  "Preparing backup" for hours after a big change (normal, first backup is full),
  NAS backups corrupting ("Time Machine must create a new backup"): move to a local disk
  or supported NAS firmware.

## Migration Assistant
- On the new Mac during Setup Assistant (or later from Applications > Utilities), choose
  transfer from a Mac, Time Machine backup or startup disk. Fastest: both Macs on the
  same network or cable (Thunderbolt/USB-C).
- Select users, apps, settings, files. Transfers the user account with the same short
  name; if the new Mac already has an account with that name, it asks to rename or
  replace.
- Managed Macs: MDM enrollment, FileVault, and apps should come from ADE and MDM, not
  migration. Prefer migrating only the user's files (or let OneDrive sync), not apps or
  system settings, to avoid carrying over old profiles, kernel extensions and junk.
- Intel to Apple silicon: Intel-only apps run via Rosetta 2; old kernel extensions won't.

## Activity Monitor triage
- CPU tab: sort by % CPU; `kernel_task` high means thermal management (the Mac is hot,
  check fans and vents, charging on the right side). `mds_stores` / `mdworker` high
  after migration = Spotlight indexing, wait.
- Memory tab: **Memory Pressure** graph matters more than free memory; red pressure
  means too little RAM for the workload; swap used climbing.
- Energy tab: apps preventing sleep; Disk tab: heavy writers; Network tab.
- Select a process > Info (i) > Sample to capture a stack for a hung app; or `sudo
  sysdiagnose` for a full diagnostic bundle.

## Verify
`tmutil latestbackup` shows a recent date, migrated user can open their files and apps,
and Activity Monitor shows normal pressure and no runaway process after the fix.
