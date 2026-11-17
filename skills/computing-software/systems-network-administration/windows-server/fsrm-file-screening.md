---
id: computing-software.systems-network-administration.windows-server.fsrm-file-screening
name: fsrm-file-screening
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, fsrm, file-server-resource-manager, file-screening, new-fsrmfilegroup, new-fsrmfilescreen, passive-screening, ransomware-extensions, command-action, file-screen-exceptions, file-groups]
level: practitioner
status: docs-checked
description: "Block unwanted or ransomware-pattern files with FSRM file screens: file groups, active vs passive screens, exceptions, and a command action that blocks the offending user."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/file-screening-management.md
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/create-file-screen.md
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/define-file-groups-for-screening.md
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmfilescreen
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmaction
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# FSRM file screening

## Concepts
- **File group**: file name patterns to include or exclude (standard wildcards, for example `*.exe`).
- **File screen** on a folder: **active** (blocks) or **passive** (audit/notify only).
- **Exception**: a subfolder where a screened group is allowed.
Screens match file name patterns, not content.

## Block media and executables in a share
```powershell
New-FsrmFileScreen -Path '<DATA_DRIVE>:\Shares\Finance' -IncludeGroup '<MEDIA_FILE_GROUP>','<EXECUTABLE_FILE_GROUP>' -Active `
  -Notification (New-FsrmAction Event -EventType Warning -Body '[Source Io Owner] tried to save [Source File Path]')
New-FsrmFileScreenException -Path '<DATA_DRIVE>:\Shares\Finance\Training' -IncludeGroup '<MEDIA_FILE_GROUP>'
```
List the built-in file group names on your server with `Get-FsrmFileGroup`.

## Ransomware canary pattern (defence in depth)
```powershell
New-FsrmFileGroup -Name 'Ransomware patterns' -IncludePattern @('<PATTERN_1>','<PATTERN_2>')   # your own tripwire names and extensions
$cmd = New-FsrmAction Command -Command '<WINDIR>\System32\WindowsPowerShell\v1.0\powershell.exe' `
  -CommandParameters '-NoProfile -File "<SCRIPTS_DIR>\Block-SmbUser.ps1" -User "[Source Io Owner]"' `
  -SecurityLevel LocalSystem -KillTimeOut 2 -WorkingDirectory '<SCRIPTS_DIR>'   # KillTimeOut is in minutes
New-FsrmFileScreen -Path '<DATA_DRIVE>:\Shares' -IncludeGroup 'Ransomware patterns' -Active:$false -Notification $cmd
```
`Block-SmbUser.ps1` would run `Block-SmbShareAccess -Name * -AccountName $User -Force` and
alert. Pattern lists go stale quickly (community-maintained lists exist); treat as a tripwire,
not prevention. EDR and backups remain the real controls.

## Gotchas
- Generate a **storage report** "Files by File Group" to find files that already match a group.
- Users can rename a blocked file to another extension; screening is policy enforcement, not security.
- Command actions run as the chosen security level (None, NetworkService, LocalService or LocalSystem); keep the scripts write-protected.

## Verify
- [ ] Saving a file matching the screened group in Finance fails (active screen) or only notifies (passive); it succeeds in Training.
- [ ] Creating a file that matches a tripwire pattern in a test share triggers the action in a lab.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- File screens: active screening blocks and notifies, passive only notifies (create-file-screen page, `-Active` / `-Active:$false`); screens apply to the folder and subfolders; exceptions via New-FsrmFileScreenException -IncludeGroup; file groups are sets of file name patterns with include/exclude and standard wildcards (define-file-groups page; New-FsrmFileGroup -IncludePattern / -ExcludePattern).
- New-FsrmAction -Type Command parameters: -SecurityLevel (None, NetworkService, LocalService, LocalSystem), -KillTimeOut in minutes, -WorkingDirectory, -CommandParameters.
- "Files by File Group" is a documented storage report. Removed unconfirmed details: the built-in group names (now placeholders), the claim that screens do not affect existing files, and the named ransomware extensions (now placeholders).

Method: documentation only; no commands were run.
