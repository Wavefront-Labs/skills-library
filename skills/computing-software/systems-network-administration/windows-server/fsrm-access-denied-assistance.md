---
id: computing-software.systems-network-administration.windows-server.fsrm-access-denied-assistance
name: fsrm-access-denied-assistance
category: computing-software
field: systems-network-administration
product: windows-server
tags: [fsrm, access-denied-assistance, file-server, dynamic-access-control, group-policy]
level: practitioner
status: docs-checked
description: "Enable access-denied assistance so users get a helpful message and a request-access email instead of a bare Access Denied on file shares."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/solution-guides/deploy-access-denied-assistance--demonstration-steps-
  - https://learn.microsoft.com/en-us/windows-server/identity/solution-guides/scenario--access-denied-assistance
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/set-fsrmadrsetting
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/set-fsrmmgmtproperty
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access-denied assistance

When a user hits a folder they cannot open, Explorer (Windows 8 and Windows Server 2012 or later) can show a custom message with a
**Request assistance** button that emails the folder owner or helpdesk with the user's details.

## Enable for clients (GPO)
Computer > Administrative Templates > System > Access-Denied Assistance:
- **Customize message for Access Denied errors** = Enabled (can set text and allow request).
- **Enable access-denied assistance on client for all file types** = Enabled.

## Configure on the file server (FSRM)
```powershell
Set-FsrmAdrSetting -Event AccessDenied -Enabled:$true `
  -DisplayMessage 'You do not have access to [Original File Path]. Use Request assistance to ask the folder owner.' `
  -AllowRequests:$true -MailToOwner:$true -MailCCAdmin:$true -IncludeDeviceClaims:$true -IncludeUserClaims:$true
Set-FsrmAdrSetting -Event FileNotFound -Enabled:$true -DisplayMessage 'File not found. It may have moved.'
```
The server-wide message lives in FSRM Options > Access-Denied Assistance. A separate message for one shared folder is set with
`Set-FsrmMgmtProperty -Namespace <DATA_VOLUME>\Shares\Finance -Name AccessDeniedMessage_MS -Value '...'`.
Macros available in messages include `[Original File Path]`, `[Original File Path Folder]`, `[Admin Email]` and `[Data Owner Email]`.

## Folder owner emails
When a user requests access the server emails the folder owner (a distribution list can be defined for shared folders); with `-MailToOwner` the request goes to the owner and with `-MailCCAdmin` it copies the administrator. SMTP must be configured in FSRM settings. The management property that holds the owner address is not named in the cmdlet reference or deployment guide, so use the FSRM console's folder management properties.

## Gotchas
- The client must run Windows 8 or later.
- The request email exposes the path and user; review for sensitive folder names.

## Verify
- [ ] Denied user sees the custom message and the request email arrives at the owner.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Deploy Access-Denied Assistance guide: GPO path Computer Configuration > Policies > Administrative Templates > System > Access-Denied Assistance with `Customize message for Access Denied errors` and `Enable access-denied assistance on client for all file types`; per-server setup via FSRM Options; per-folder message with `Set-FsrmMgmtProperty -Namespace ... -Name AccessDeniedMessage_MS`; verified with a Windows 8 client; message macros.
- Set-FsrmAdrSetting reference: -Event AccessDenied|FileNotFound, -AllowRequests, -MailToOwner, -MailCCAdmin, -IncludeDeviceClaims, -IncludeUserClaims are switch parameters, so the examples now use the `-Parameter:$true` form.
- Removed unconfirmed details: the `FolderOwnerEmail_MS` property name and the "only SMB shares on the FSRM server" limit.

Method: documentation only; no commands were run.
