---
id: computing-software.systems-network-administration.windows-server.wac-kerberos-delegation
name: wac-kerberos-delegation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-admin-center, wac, wac-kerberos-delegation, resource-based-constrained-delegation, single-sign-on]
level: advanced
status: docs-checked
description: "Configure resource-based constrained delegation so Windows Admin Center gateway users get single sign-on to targets without CredSSP or repeated credential prompts."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/user-access-control
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/support/troubleshooting
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kerberos delegation for the WAC gateway

With WAC installed as a gateway, the user's browser authenticates to the gateway, and the gateway must then
connect to target servers **as the user**. Without delegation the user gets a "Manage as" credential prompt for
every server.

## Configure RBCD on each target (or on targets in bulk)
```powershell
$gw = Get-ADComputer WACGW01
Get-ADComputer -Filter * -SearchBase "OU=Servers,DC=corp,DC=example,DC=com" | ForEach-Object {
  Set-ADComputer $_ -PrincipalsAllowedToDelegateToAccount $gw }
```
The documented single-target form is `Set-ADComputer -Identity (Get-ADComputer node01) -PrincipalsAllowedToDelegateToAccount (Get-ADComputer wac)`.
RBCD lives on the **target** computer object. Setting the property replaces the existing value (the
`msDS-AllowedToActOnBehalfOfOtherIdentity` attribute), so read and merge first if a target already allows other front ends.
Remove the relationship with `-PrincipalsAllowedToDelegateToAccount $null`.
When WAC is installed on Windows 10 it is ready for SSO; on Windows Server you must set up Kerberos delegation yourself.

## For a highly available gateway
The docs do not describe delegation for the clustered gateway; test with the cluster's client access point computer account and the nodes before relying on it.

## Things that block SSO
- Group-based access is not supported in workgroups or across non-trusted domains.
- The connecting user needs administrative rights on the target (passed-through Windows credential or **Manage as**).
- If delegation is not configured, users get a credential prompt and must use **Manage as**.

## Verify
- [ ] Open a target in WAC without a credential prompt.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (troubleshooting ms.date 2025-06-24; Azure VM and Arc pages current in repo), Windows Admin Center 2410+.
Confirmed from configure/user-access-control (ms.date 2025-06-26, Configure single sign-on section): the RBCD Set-ADComputer example, removal with $null, need for delegation on Windows Server versus Windows 10,
and the group-access limitation; support/troubleshooting for the delegation and Manage as behaviour.
Removed klist purge, Protected Users, IP/CNAME NTLM fallback, cross-forest and event 4624 claims, and the cluster CNO assertion, none of which the pages state.
Method: documentation only; no commands were run.
