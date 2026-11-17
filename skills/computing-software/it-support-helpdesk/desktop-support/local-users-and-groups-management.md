---
id: computing-software.it-support-helpdesk.desktop-support.local-users-and-groups-management
name: local-users-and-groups-management
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-admin-tools, local-users-groups, lusrmgr, net-localgroup, local-administrators, get-localuser, built-in-administrator, comptia-a-plus]
level: practitioner
status: draft
description: "Manage local accounts and groups on Windows: lusrmgr.msc, net user/localgroup, PowerShell LocalAccounts, who is in local Administrators, and why local accounts should be rare."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-localgroup"
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/access-control/local-accounts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# local-users-and-groups-management

Goal: know and control which local accounts exist and who has local admin
(A+ 220-1202 1.4 Local Users and Groups).

## Look
```powershell
Get-LocalUser | Select Name, Enabled, LastLogon, PasswordLastSet
Get-LocalGroupMember -Group Administrators
```
```cmd
net user
net localgroup administrators
```
`lusrmgr.msc` — not available on Home editions (use Settings → Accounts or
`net user`).

## Common tasks
```powershell
# temporary local account for a kiosk/test (avoid on managed PCs)
New-LocalUser -Name 'kiosk' -Password (Read-Host -AsSecureString) -AccountNeverExpires
Add-LocalGroupMember -Group 'Users' -Member 'kiosk'
# remove someone's local admin
Remove-LocalGroupMember -Group Administrators -Member 'CORP\jdoe'
Disable-LocalUser -Name 'olduser'
```
Domain/Entra users and groups can be members of local groups
(`AzureAD\user@contoso.com`, `CORP\Group`).

## Managed fleet practice
- Local Administrators membership managed centrally: Intune **Account
  protection → Local user group membership** policy, or GPO Restricted
  Groups / Group Policy Preferences; LAPS manages the one local admin
  account's password (see Windows LAPS).
- Built-in Administrator disabled (or managed by LAPS); no shared local
  admin passwords.
- Standard users by default; temporary elevation via EPM/approved tool.

## Gotchas
- Removing the last admin account locks you out of local admin tasks —
  ensure LAPS/another admin path first.
- Entra-joined devices: the user who joined the device becomes local admin
  by default unless the Autopilot profile sets "standard user".
- Changes you make locally get reverted by policy at next refresh — check
  what policy enforces.

## Verify
`Get-LocalGroupMember Administrators` returns only approved members (LAPS
account, admin groups), matching policy on a sample of devices.
