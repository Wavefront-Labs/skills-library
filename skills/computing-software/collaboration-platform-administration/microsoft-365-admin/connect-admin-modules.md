---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.connect-admin-modules
name: connect-admin-modules
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [connect-admin-modules, m365-powershell]
level: practitioner
status: draft
description: Install and connect Microsoft Graph, Exchange Online, Teams and SharePoint modules with least scopes.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connect to the admin PowerShell modules
**Goal:** Install and connect Microsoft Graph, Exchange Online, Teams and SharePoint modules with least scopes.

- `Install-Module Microsoft.Graph -Scope CurrentUser`; `Connect-MgGraph -Scopes 'User.Read.All'`.
- `Install-Module ExchangeOnlineManagement`; `Connect-ExchangeOnline -UserPrincipalName <admin>`.
- `Install-Module MicrosoftTeams`; `Connect-MicrosoftTeams`.
- `Install-Module Microsoft.Online.SharePoint.PowerShell`; `Connect-SPOService -Url https://<tenant>-admin.sharepoint.com`.
- Use `Disconnect-` cmdlets when finished; use PowerShell 7 where supported.

## Gotchas
- The old MSOnline and AzureAD modules are deprecated; use Microsoft Graph PowerShell for new scripts.
- Scopes are consented per app; grant only what the task needs.

## Self-check
`Get-MgContext` shows the expected account and scopes.
