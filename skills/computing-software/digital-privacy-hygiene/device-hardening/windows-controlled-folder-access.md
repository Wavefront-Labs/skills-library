---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-controlled-folder-access
name: windows-controlled-folder-access
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, controlled-folder-access, ransomware-protection, windows, microsoft-defender, set-mppreference]
level: practitioner
status: docs-checked
description: "Turn on Controlled folder access in Audit Mode first, then enforce it, add protected folders and allowed apps, and handle blocked apps."
sources:
  - "https://learn.microsoft.com/en-us/defender-endpoint/enable-controlled-folders"
  - "https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows Controlled folder access

**Goal:** only trusted apps may change files in protected folders, so untrusted software (including ransomware) is blocked.

## Modes
Modes include **Enabled** (value 1), **Audit Mode** (2: untrusted apps can change files but attempts are recorded) and
**Audit disk modification only** (4). Microsoft recommends running Audit Mode first, allowing the apps your users need,
then moving to Enabled. The Windows Security app supports only On (Enabled) and Off; use PowerShell for Audit Mode.

## Protected folders
Defaults include Documents, Favorites, Music, Pictures, Videos under the user profile and the Public equivalents. If a
folder is redirected (for example by OneDrive Known Folder Move), the redirected location is protected. Add more folders
and allow trusted apps through the Windows Security app; **Recently blocked apps** lists apps to allow.

## PowerShell (administrator)
```powershell
Set-MpPreference -EnableControlledFolderAccess AuditMode     # test first
Set-MpPreference -EnableControlledFolderAccess Enabled
Add-MpPreference -ControlledFolderAccessProtectedFolders "<PHOTOS_DIR>"
Add-MpPreference -ControlledFolderAccessAllowedApplications "<APP_DIR>\app.exe"
```
Set-MpPreference overwrites existing protected folders and allowed apps; Add-MpPreference adds without affecting existing
values and Remove-MpPreference removes entries.

## Rolling it out
Run Audit Mode on a busy PC, review what would have been blocked, allow legitimate apps, then enforce.

## Limits
Keep versioned, offline or cloud backups as your real recovery path; this feature does not replace backups.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Controlled folder access overview and configure pages): modes and values, Audit
Mode recommendation, Windows Security app limits, default folder list (partly), Recently blocked apps, cmdlet syntax and
overwrite behaviour. Removed (not on the fetched pages): the Event Viewer event IDs, Desktop as a default, the Windows
Security menu path, Defender-only requirement, exfiltration and OneDrive Files Restore notes.
Method: documentation only; no commands were run.
