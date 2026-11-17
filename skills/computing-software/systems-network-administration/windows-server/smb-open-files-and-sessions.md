---
id: computing-software.systems-network-administration.windows-server.smb-open-files-and-sessions
name: smb-open-files-and-sessions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, file-server, smb-shares, get-smbopenfile, close-smbopenfile, smb-sessions, get-smbsession, close-smbsession, locked-files, openfiles, file-locks]
level: practitioner
status: docs-checked
description: "Find who has a file open on a Windows file server and release it safely: Get-SmbOpenFile/Close-SmbOpenFile, sessions per user, and when closing loses data."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbopenfile
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/close-smbopenfile
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/close-smbsession
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbsession
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB open files and sessions

**Typical ticket:** "File is locked for editing by another user" or a deployment cannot
replace a file on a share.

## Find the lock
```powershell
Get-SmbOpenFile -CimSession fs01 | ? Path -like '*\Finance\Budget2026.xlsx' |
  Select FileId,SessionId,ClientUserName,ClientComputerName,Path,ShareRelativePath
Get-SmbOpenFile -CimSession fs01 -ClientUserName 'AD\jsmith'
```

## Release it
1. Ask the user to close the file (data safety).
2. Otherwise close the handle:
```powershell
Close-SmbOpenFile -CimSession fs01 -FileId 1236110135393 -Force
```
Unsaved changes on the client are lost and the app may show errors. For a stale session
(laptop slept/left), close the whole session:
```powershell
Get-SmbSession -CimSession fs01 | ? ClientUserName -eq 'AD\jsmith' | Select SessionId,ClientComputerName,NumOpens
Close-SmbSession -CimSession fs01 -SessionId 1236110135297 -Force
```

## GUI
Computer Management > Shared Folders > Open Files / Sessions.

## Clusters and DFS
- On a clustered file server, query the role's owner node (or use the client access point name in `-CimSession`).
- DFS namespaces: find the actual target server first; the open handle lives on the target, not the namespace server.

## Verify
- [ ] The file can be renamed/replaced after closing; user informed.
- [ ] Repeated stale-lock tickets trigger a look at client sleep/offline-files settings.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Get-SmbOpenFile: -CimSession, -ClientUserName, -ClientComputerName, -FileId, -SessionId; output includes FileId, SessionId, Path, ShareRelativePath, ClientComputerName, ClientUserName.
- Close-SmbOpenFile takes -FileId, -SessionId and -Force (no confirmation); Close-SmbSession and Get-SmbSession (SessionId, ClientComputerName, ClientUserName, NumOpens) reference pages.
- Removed unconfirmed details: the SecondsIdle property, Office lock file commentary, the `openfiles` command notes and the dfsutil command.

Method: documentation only; no commands were run.
