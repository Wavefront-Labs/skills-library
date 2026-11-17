---
id: computing-software.it-support-helpdesk.remote-support-tools.shadowing-rds-sessions
name: shadowing-rds-sessions
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rdp-shadow, rds, remote-desktop, session-shadowing, mstsc, qwinsta]
level: practitioner
status: draft
description: "Shadow a user's RDS or console session with mstsc /shadow: find the session ID, set the remote-control policy, open the right firewall rules, and respect consent."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/shadow"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/qwinsta"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# shadowing-rds-sessions

## Find the session
```cmd
qwinsta /server:RDSH01
```
Note the ID for the user (state Active). In a farm, find the host first in Server
Manager > Collections or with `Get-RDUserSession -ConnectionBroker <broker>`.

## Connect
```cmd
mstsc /v:RDSH01 /shadow:3 /control
```
- Omit `/control` for view only.
- `/noConsentPrompt` skips the user prompt only if policy allows it; get consent anyway
  unless policy and an approved reason say otherwise.
- Works against Windows 10/11 console sessions too (session usually 1 or 2).

## Policy (who may do what)
GPO: Computer Configuration > Administrative Templates > Windows Components > Remote
Desktop Services > Remote Desktop Session Host > Connections > "Set rules for remote
control of Remote Desktop Services user sessions". Registry value `Shadow` under
`HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services`:

| Value | Meaning |
|---|---|
| 0 | No remote control |
| 1 | Full control with user's permission |
| 2 | Full control without permission |
| 3 | View with user's permission |
| 4 | View without permission |

## Requirements
- You are a local admin on the host, or have been granted remote control permission on
  the RDP-Tcp listener.
- Firewall on the target: "Remote Desktop - Shadow (TCP-In)" rule enabled plus SMB (445)
  and RPC dynamic ports for the session query.

## Gotchas
- "Shadow error: The version of Windows running on this server does not support user
  shadowing" usually means the firewall rule is off, not the OS.
- Multi-monitor users: the shadow window shows all their monitors scaled into one.
- Ending: close the window; the user is not logged off.

## Verify
The user sees the consent prompt (when required), you see their live session, and the
ticket records consent and duration.
