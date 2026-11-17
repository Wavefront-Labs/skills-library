---
id: computing-software.systems-network-administration.windows-server.rds-session-shadowing-and-management
name: rds-session-shadowing-and-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [remote-desktop-services, rds-shadowing, qwinsta, session-management, group-policy]
level: practitioner
status: docs-checked
description: "Shadow and manage RDS user sessions: mstsc /shadow with consent policy, qwinsta/rwinsta/logoff, sending messages and Get-RDUserSession from the broker."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/query-user
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reset-session
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/msg
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/invoke-rduserlogoff
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/send-rdusermessage
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdsessionhost
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/shadow-terminal-server-session
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS session shadowing and management

## List sessions
```cmd
query user /server:RDSH01
```
```powershell
Get-RDUserSession -ConnectionBroker RDCB01.corp.example.com
```

## Shadow (helpdesk view or control)
```cmd
mstsc /v:RDSH01 /shadow:3 /control
mstsc /v:RDSH01 /shadow:3 /noConsentPrompt /control
```
- `/shadow:<SessionId>`; `/control` allows control of the session (otherwise view only); `/noConsentPrompt` allows
  shadowing without user consent.
Policy: the Group Policy setting **Set rules for remote control of Remote Desktop Services user sessions** (Remote Desktop
Session Host > Connections) has the options Full Control with or without the user's permission; agree and document a
justification before choosing the option without permission. Shadowing a console session or your own session is not
possible, and a session that is disconnected or has no logged-on user cannot be shadowed.

## Log off, reset, message
```cmd
logoff 3 /server:RDSH01
reset session 3 /server:RDSH01      :: reset a hung session
msg * /server:RDSH01 "Server restarts at 22:00, please save your work"
```
```powershell
Invoke-RDUserLogoff -HostServer RDSH01.corp.example.com -UnifiedSessionId 3 -Force
Send-RDUserMessage -HostServer RDSH01.corp.example.com -UnifiedSessionId 3 -MessageTitle 'Maintenance' -MessageBody 'Restart at 22:00'
```

## Drain a host before maintenance
`Set-RDSessionHost -SessionHost RDSH01.corp.example.com -NewConnectionAllowed NotUntilReboot -ConnectionBroker <broker FQDN>`

## Verify
- [ ] Helpdesk can shadow with consent; drain mode stops new logons.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in the command references: mstsc /v, /shadow, /control and /noConsentPrompt; query user, logoff and reset session syntax with /server; msg syntax including * and /server; Invoke-RDUserLogoff (-HostServer, -UnifiedSessionID, -Force), Send-RDUserMessage (-MessageTitle, -MessageBody), Get-RDUserSession and Set-RDSessionHost -NewConnectionAllowed values; the remote control policy options and shadow limitations from the support articles. Removed as unconfirmed: qwinsta and rwinsta (replaced by documented query user and reset session), the SMB 445 and dynamic RPC firewall note, the WMI AddAccount permission command, and the Select property list for Get-RDUserSession.

Method: documentation only; no commands were run.
