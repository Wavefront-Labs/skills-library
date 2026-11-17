---
id: computing-software.systems-network-administration.windows-server.system-state-and-bare-metal-backup
name: system-state-and-bare-metal-backup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-backup, wbadmin, system-state-backup, bare-metal-recovery, critical-volumes, windows-server-backup-feature]
level: practitioner
status: docs-checked
description: "Back up Windows Server system state and bare-metal recovery images with wbadmin: targets, schedules, retention, and restoring system state."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-systemstatebackup
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System state and bare-metal backups with wbadmin

## One-off backups
```powershell
wbadmin start systemstatebackup -backupTarget:E: -quiet
wbadmin start backup -backupTarget:\\nas01\wsb\SRV01 -allCritical -systemState -vssFull -quiet   # bare metal
```
- `-allCritical` includes every volume holding OS/boot/system-state components: required
  for bare-metal recovery (BMR).
- Network share targets keep only the latest backup (the older one is overwritten).

## System state restore (non-DC)
```powershell
wbadmin get versions
wbadmin start systemstaterecovery -version:10/15/2026-21:00 -quiet
```

## Verify
- [ ] `wbadmin get versions` shows recent versions.

## Checked
2026-10-28: Confirmed on Learn pages wbadmin-start-backup, wbadmin-start-systemstatebackup, wbadmin-start-systemstaterecovery and wbadmin-get-versions: -backupTarget, -allCritical (needed for bare metal recovery), -systemState, -vssFull, systemstaterecovery -version, get versions, network-share overwrite behaviour. Removed: feature install line, multi-version VSS claim, tombstone 180-day claim, WB* scheduling cmdlets, WinRE restore steps, disk-size claim, DSRM note.
Method: documentation only; no commands were run.
