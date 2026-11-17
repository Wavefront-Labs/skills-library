---
id: computing-software.systems-network-administration.windows-server.dfs-namespace-modes-and-migration
name: dfs-namespace-modes-and-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs, dfsn-windows-server-2008-mode, domain-based-namespace, access-based-enumeration, dfsutil]
level: advanced
status: docs-checked
description: "Choose DFS namespace modes (domain-based Windows Server 2008 mode vs Windows 2000 mode vs standalone) and migrate an old namespace to 2008 mode without breaking paths."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/choose-a-namespace-type
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/migrate-a-domain-based-namespace-to-windows-server-2008-mode
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/enable-access-based-enumeration-on-a-namespace
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/new-dfsnroot
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/grant-dfsnaccess
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFS namespace modes

| Type | Scale | Needs | Notes |
|---|---|---|---|
| Standalone | recommended limit 50,000 folders with targets; info kept in the registry | AD DS not required | path `\\server\ns` |
| Domain-based, Windows 2000 mode | AD object under 5 MB, about 5,000 folders with targets | forest Windows 2000, domain Windows 2000 mixed | no ABE |
| Domain-based, **Windows Server 2008 mode** | recommended limit 50,000 folders with targets | forest Windows Server 2003, domain Windows Server 2008, 2008+ namespace servers | ABE, increased scalability; choose when supported |

## Check the mode
```powershell
Get-DfsnRoot -Path \\ad.example.com\files | Select Path,Type,State
```
`dfsutil root` can also display a root; the same command group creates, removes, imports and exports roots.
`Type` DomainV2 = 2008 mode, DomainV1 = 2000 mode.

## Migrate 2000 mode to 2008 mode
There is no in-place switch. Recreate with the same name:
```cmd
dfsutil root export \\ad.example.com\files <BACKUP>\files.xml
REM write down the path of every namespace server: dfsutil cannot import namespace servers
dfsutil root remove \\ad.example.com\files
REM recreate in 2008 mode with the same name (DFS Management), or:
dfsutil root adddom \\FS01\files v2
dfsutil root import merge <BACKUP>\files.xml \\ad.example.com\files
REM add remaining namespace servers
dfsutil target add \\FS02\files
```
Clients cache root referrals for 300 seconds by default. To shorten the import of a large namespace, run `dfsutil root import` locally on a namespace server.

## Enable access-based enumeration (2008 mode)
```powershell
Set-DfsnRoot -Path \\ad.example.com\files -EnableAccessBasedEnumeration $true
Grant-DfsnAccess -Path \\ad.example.com\files\Finance -AccountName 'AD\GG-Finance'
```
ABE needs all namespace servers on Windows Server 2008 or newer and a Windows Server 2008 mode namespace; it can raise CPU use on busy servers. It does not stop a referral to a target whose path is already known; the target's share and NTFS permissions do.

## Verify
- [ ] `Get-DfsnRoot` Type DomainV2 and every folder resolves to its targets (`dfsutil diag`, see `dfsutil diag /?`).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: the namespace type comparison table (size, functional levels, namespace server versions, ABE support); the export, remove, `adddom ... v2`, `import merge` and `target add` migration steps and the note that dfsutil cannot import namespace servers; 300-second root referral cache; ABE prerequisites and its CPU note; `Type` values DomainV1/DomainV2. Corrected the size figures (the 2008-mode and standalone limits are recommended limits of 50,000 folders with targets), the wrong `dfsutil root import set` step and the missing `adddom ... v2` step; removed the `dfsutil property sd grant` line.

Method: documentation only; no commands were run.
