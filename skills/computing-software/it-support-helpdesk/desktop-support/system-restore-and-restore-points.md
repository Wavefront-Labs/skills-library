---
id: computing-software.it-support-helpdesk.desktop-support.system-restore-and-restore-points
name: system-restore-and-restore-points
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, system-restore, restore-points, rstrui, checkpoint-computer, volume-shadow-copy, vssadmin, windows-recovery, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Use System Restore properly: enable protection, create restore points before risky changes, roll back from Windows or WinRE, and know what it does and doesn't revert."
sources:
  - "https://support.microsoft.com/en-us/windows/experience/backup-recovery/system-protection"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/checkpoint-computer"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin-resize-shadowstorage"
  - "https://learn.microsoft.com/en-us/windows/win32/sr/calling-srsetrestorepoint"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# system-restore-and-restore-points

Goal: undo a bad driver, app or registry change in minutes, and make sure a
restore point exists before you need one.

## What it reverts / does not
- Reverts: system files, installed applications, registry and system settings
  to the state at the restore point.
- Does **not** revert personal files. It is not a backup: it is meant to
  recover from system problems, so keep real backups of data.
- System protection is not enabled by default and is configured per drive,
  so check it before promising a rollback.

## Enable and size
```powershell
Enable-ComputerRestore -Drive "$env:SystemDrive\"
vssadmin resize shadowstorage /for=C: /on=C: /maxsize=10GB
vssadmin list shadows
```
`/maxsize` takes a size with a unit (KB, MB, GB and so on, at least 1 MB), not
a percentage; with no value the space is unlimited. In the GUI: System
Properties, System Protection tab, Configure.

## Create a point before risky work
```powershell
Checkpoint-Computer -Description "Before VPN client 7.2" -RestorePointType MODIFY_SETTINGS
```
Valid types: APPLICATION_INSTALL (the default), APPLICATION_UNINSTALL,
DEVICE_DRIVER_INSTALL, MODIFY_SETTINGS, CANCELLED_OPERATION. Windows creates
at most one restore point per 24 hours by default; a second request returns
"A new system restore point cannot be created because one has already been
created within the past 24 hours". The throttle is controlled by the DWORD
`SystemRestorePointCreationFrequency` under
`HKLM\Software\Microsoft\Windows NT\CurrentVersion\SystemRestore`
(absent by default): 0 means never skip, N means skip if one was made in the
last N minutes. Back up the key before editing the registry.

## Roll back
- From Windows: Create a restore point (Start search), System Protection tab,
  System Restore.
- WinRE also offers System Restore when Windows will not boot; it needs
  restore points to exist.
- If System Restore fails with 0x8007045b or a similar error, see Microsoft's
  article for that error.

## Verify
After reboot the symptom is gone and `Get-ComputerRestorePoint` lists the
restore points you expect.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Checkpoint-Computer, vssadmin resize shadowstorage, WinRE technical reference and Win32 System Restore pages, Microsoft Support System Protection page, as published October 2026 (Windows 10/11). Confirmed: reverts system files, apps, registry and settings but not personal files; System Protection configuration and manual creation steps; Checkpoint-Computer types and 24-hour throttle message; SystemRestorePointCreationFrequency key, path and value meaning; vssadmin /maxsize needs a unit. Removed: percentage /maxsize (wrong), failure codes 0x80070091 and 0x8000ffff, restore-of-a-restore claims, disk clean-up and feature-update effects, domain trust repair advice.

Method: documentation only; no commands were run.
