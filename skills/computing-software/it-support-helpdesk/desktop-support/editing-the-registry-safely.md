---
id: computing-software.it-support-helpdesk.desktop-support.editing-the-registry-safely
name: editing-the-registry-safely
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-admin-tools, regedit, registry, reg-export, reg-add, hkcu-vs-hklm, registry-permissions, policy-keys, ntuser-dat, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Change the Windows registry without breaking things: backup with reg export, HKLM vs HKCU vs policy keys, reg.exe and PowerShell, editing another user's hive, and when not to."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/windows-registry-advanced-users"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-export"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-add"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-load"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-itemproperty"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# editing-the-registry-safely

Goal: apply a documented registry fix with a way back, to the right hive and
user.

Microsoft's warning applies: editing the registry incorrectly can cause
serious problems, so back up first and follow vendor documentation exactly.

## Before editing
- Is the setting available through Group Policy, Intune or the app's own
  settings? Use that instead of a direct edit.
- Source: vendor or Microsoft documentation for the exact key, value name,
  type and data. Not a forum guess.
- **Back up the key** (and know how to restore it):
  ```cmd
  reg export "HKLM\SOFTWARE\Vendor\App" %TEMP%\vendor-app-backup.reg /y
  ```
  Restore by double-clicking the .reg file, or `reg import`. `/y` overwrites
  an existing file without prompting. For broader changes also create a
  restore point (see the `system-restore-and-restore-points` skill).

## Hives
| Hive | Scope |
|---|---|
| HKLM\SOFTWARE | machine-wide; needs admin |
| HKCU | the signed-in user only (the account running regedit) |
| HKEY_USERS | all actively loaded user profiles; HKCU is a subkey of it |
| HKLM\SOFTWARE\WOW6432Node | where 64-bit Windows shows 32-bit application keys |
Running regedit elevated as a different admin account edits **that admin's**
HKCU, not the user's: a classic mistake.

## Edit
```cmd
reg add "HKLM\SOFTWARE\Vendor\App" /v LogLevel /t REG_DWORD /d 2 /f
reg query "HKLM\SOFTWARE\Vendor\App" /v LogLevel
reg delete "HKLM\SOFTWARE\Vendor\App" /v OldSetting /f
```
```powershell
New-ItemProperty -Path 'HKLM:\SOFTWARE\Vendor\App' -Name LogLevel -PropertyType DWord -Value 2 -Force
```

## Another user's settings
- Signed in: their hive is under `HKEY_USERS\<SID>` (find the SID with
  `Get-CimInstance Win32_UserProfile`).
- Not signed in: load their `NTUSER.DAT` under HKEY_USERS (regedit File, Load
  Hive, or `reg load`), edit, then **unload** it (`reg unload`) so the file is
  released.

## Gotchas
- Value types matter (REG_DWORD vs REG_SZ); use the type the documentation
  names.
- Some changes need sign-out, a service restart or a reboot.
- Settings managed by policy may be re-applied by the management tool.

## Verify
`reg query` shows the intended value; the behaviour changes after any
required restart; the backup file is attached to the ticket.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn registry for advanced users, reg export/add/delete/query/load/unload/import and New-ItemProperty pages as published October 2026. Confirmed: back-up-before-editing guidance, export of subkeys and restore by double-clicking the .reg file, reg export /y behaviour, HKEY_USERS and HKCU relationship, WOW6432Node 32-bit key location, REG_DWORD description, reg add/delete/query syntax, New-ItemProperty -PropertyType. Removed: registry-cleaner and key-permission remarks, the claim that policy keys are always overwritten, and the exam-objective reference.

Run 2026-11-01 (read-only on HKCU\Environment): `reg query <key> /v <name>` printed the value; `reg export <key> <file> /y` wrote a .reg file; the same export without `/y` onto an existing file waits for an overwrite confirmation (it hung the non-interactive run), which matches the `/y` description. `reg add`, `reg delete`, `reg import`, `reg load` and `New-ItemProperty` were not run (they write to the registry), so the skill stays docs-checked.
Method: documentation plus read-only commands.
