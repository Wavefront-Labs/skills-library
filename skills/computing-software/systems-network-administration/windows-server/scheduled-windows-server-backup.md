---
id: computing-software.systems-network-administration.windows-server.scheduled-windows-server-backup
name: scheduled-windows-server-backup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server-backup, wbadmin-schedule, system-state-backup, backup-retention, bare-metal-recovery]
level: practitioner
status: docs-checked
description: "Schedule Windows Server Backup: dedicated disk vs network share targets, retention behaviour, VSS full vs copy, and email alerts on failure."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-enable-backup
  - https://learn.microsoft.com/en-us/powershell/module/windowsserverbackup/set-wbpolicy
  - https://learn.microsoft.com/en-us/powershell/module/windowsserverbackup/add-wbbackuptarget
  - https://learn.microsoft.com/en-us/powershell/module/windowsserverbackup/set-wbvssbackupoption
  - https://learn.microsoft.com/en-us/powershell/module/windowsserverbackup/get-wbsummary
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled Windows Server Backup

## Targets compared
| Target | Behaviour (documented) |
|---|---|
| Disk | formatted before use; any existing data is permanently erased |
| Volume | selectable as a target; you can add several disks or volumes with one `Add-WBBackupTarget` call each |
| Network share (UNC) | only one shared folder can be used and you cannot add more locations; **the backup is overwritten** when the same computer backs up to the same folder again, and a failed run can leave no usable backup |
## PowerShell policy
```powershell
$p = New-WBPolicy
Add-WBSystemState -Policy $p
Add-WBBareMetalRecovery -Policy $p
Add-WBVolume -Policy $p -Volume (Get-WBVolume -VolumePath D:)
$disk = Get-WBDisk | Where-Object DiskNumber -eq 2
$target = New-WBBackupTarget -Disk $disk -Label 'WSB-Target'
Add-WBBackupTarget -Policy $p -Target $target
Set-WBSchedule -Policy $p -Schedule 21:00, 03:00
Set-WBVssBackupOption -Policy $p -VssFullBackup      # VSS full backup; logs may be truncated
Set-WBPolicy -Policy $p -Force                       # a disk target is formatted
```
Use `-VssCopyBackup` instead if another product backs up apps on the same volumes: a full VSS backup can break that product's incremental or differential history.

## wbadmin equivalent (find the disk identifier with `wbadmin get disks`)
```cmd
wbadmin enable backup -addtarget:<disk identifier> -schedule:21:00,03:00 -allCritical -systemState -include:D: -vssFull -quiet
wbadmin get versions
```

## Monitoring
`Get-WBSummary` returns the history of backup operations: next scheduled backup, details of the last backup and of the
last successful backup. You must be in the Administrators or Backup Operators group.

## Gotchas
- Without `-vssFull`, `wbadmin` makes a copy backup and file history is not updated.

## Verify
- [ ] `Get-WBSummary` shows a recent last successful backup.

## Checked

2026-10-26 against the wbadmin enable backup reference (windowsserverdocs, last commit 2026-10-23) and the WindowsServerBackup module reference for Windows Server 2025 (windows-powershell-docs): -addtarget, -schedule (HH:MM, comma delimited), -systemState, -allCritical, -include, -vssFull, -vssCopy, -quiet, disk formatting and erasure, single shared-folder target and overwrite behaviour, Set-WBPolicy, Set-WBSchedule, Add-WBBackupTarget, Add-WBSystemState, Add-WBBareMetalRecovery, Add-WBVolume, Get-WBSummary. Corrected the cmdlet name Set-WBVssBackupOption (the skill had Set-WBVssBackupOptions). Removed unconfirmed claims about retention by target type, the 1.5x disk size, disk rotation, one policy per server, backup event IDs and the Get-WBSummary property names.

Method: documentation only; no commands were run.
