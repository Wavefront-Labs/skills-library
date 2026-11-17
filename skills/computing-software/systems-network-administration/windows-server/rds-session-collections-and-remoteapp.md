---
id: computing-software.systems-network-administration.windows-server.rds-session-collections-and-remoteapp
name: rds-session-collections-and-remoteapp
category: computing-software
field: systems-network-administration
product: windows-server
tags: [remote-desktop-services, remoteapp, session-collections, rd-session-host, rd-connection-broker]
level: practitioner
status: docs-checked
description: "Create RDS session collections and publish RemoteApp programs with PowerShell: user groups, session limits, user profile disks vs FSLogix, and file type associations."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-create-collection
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/new-rdsessioncollection
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdsessioncollectionconfiguration
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/new-rdremoteapp
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdremoteapp
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdfiletypeassociation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS session collections and RemoteApp

## Collection
```powershell
Import-Module RemoteDesktop
New-RDSessionCollection -CollectionName 'Finance Apps' -SessionHost RDSH01.corp.example.com,RDSH02.corp.example.com `
  -ConnectionBroker RDCB01.corp.example.com -CollectionDescription 'Finance RemoteApps'
Set-RDSessionCollectionConfiguration -CollectionName 'Finance Apps' -UserGroup 'CORP\RDS-Finance' `
  -DisconnectedSessionLimitMin 120 -IdleSessionLimitMin 60 -AutomaticReconnectionEnabled $true -ConnectionBroker RDCB01.corp.example.com
```
Create separate collections when app sets or user groups differ.

## Publish RemoteApps
```powershell
New-RDRemoteApp -CollectionName 'Finance Apps' -DisplayName 'Sage' -FilePath '<APP_DIR>\Sage\sage.exe' -ConnectionBroker RDCB01.corp.example.com
Set-RDRemoteApp -CollectionName 'Finance Apps' -Alias sage -UserGroups 'CORP\Sage-Users' -ShowInWebAccess $true
Get-RDRemoteApp -CollectionName 'Finance Apps'
```
Install the application identically on every session host in the collection (same path) before publishing.

## File type associations
`Set-RDFileTypeAssociation` controls whether users can open a RemoteApp by double-clicking a file of that type
(`-IsPublished $True`); set it to `$False` to keep an extension opening in the local application.

## Profiles
User Profile Disks are configured per collection with a file share location (Create collection wizard). For other
profile options see the FSLogix skill.

## Clients
Users reach published apps through RD Web Access or the RD web client.

## Verify
- [ ] Member of Sage-Users sees the app in RD Web and it launches on either host; non-members do not see it.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in the windows-powershell-docs reference: New-RDSessionCollection, Set-RDSessionCollectionConfiguration (-UserGroup, -DisconnectedSessionLimitMin, -IdleSessionLimitMin, -AutomaticReconnectionEnabled), New-RDRemoteApp, Set-RDRemoteApp (-Alias, -UserGroups, -ShowInWebAccess), Get-RDRemoteApp and Set-RDFileTypeAssociation (IsPublished); user profile disk share in the create collection article. Removed as unconfirmed: the one collection per session host rule, install mode commands, the webfeed.aspx URL, and the FSLogix-is-recommended statement.

Method: documentation only; no commands were run.
