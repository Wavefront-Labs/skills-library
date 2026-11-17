---
id: computing-software.systems-network-administration.powershell.jea-security-pitfalls
name: jea-security-pitfalls
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, jea-security, role-capability, privilege-escalation]
level: advanced
status: docs-checked
description: "Avoid JEA designs that hand out admin: wildcard visible commands, FileSystem and Certificate providers, runspace-creating cmdlets, TypeData, run-as choices, WinRM ACL."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/security-considerations
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/role-capabilities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JEA security pitfalls

The virtual and group-managed service accounts behind a JEA session can have unrestricted access to the local machine. Role capabilities limit which commands run in that privileged context; a badly designed role lets a user break out.

## Wildcards
`VisibleCmdlets = 'Microsoft.PowerShell.Management\*-Process'` also exposes `Start-Process`, which can start an arbitrary program (even from a file share) with full administrator permissions. List `Get-Process` and `Stop-Process` explicitly instead. Avoid wildcards and audit effective permissions regularly.

## Dangerous commands (role-capabilities page)
- Admin escalation: `Add-ADGroupMember`, `Add-LocalGroupMember`, `net.exe`, `dsadd.exe`.
- Arbitrary code: `Start-Process`, `New-Service`, `Invoke-Item`, `Invoke-WmiMethod`, `Invoke-CimMethod`, `Invoke-Expression`, `Invoke-Command`, `New-ScheduledTask`, `Register-ScheduledJob`.
- `net.exe` is dangerous because `net group Administrators <user> /add` works; `Get-SmbShare` is the narrower alternative for shares.

## Best-practice warnings (security page)
- Do not allow the FileSystem provider (writable file system can bypass security) or the Certificate provider (private key access).
- Do not allow commands that create new runspaces. The `*-Job` cmdlets can, and PowerShell 7's Windows Compatibility feature runs commands in a new runspace.
- Do not expose `Update-TypeData`, `Remove-TypeData` or `Update-FormatData`: ScriptProperty and ScriptBlock members might be evaluated in FullLanguage even when the session is more restrictive.
- Do not allow `Trace-Command`; it brings all traced commands into the session.
- Do not write your own versions of the restricted proxy commands: `Exit-PSSession`, `Get-Command`, `Get-FormatData`, `Get-Help`, `Measure-Object`, `Out-Default`, `Select-Object`.
- Custom function bodies run unconstrained, so validate parameters and do not pass input to `Invoke-Expression`.

## Run-as account
- Virtual accounts are recommended: temporary, per session, credentials unknown to the user, usable only in the session. By default they are local Administrators (Domain Admins on a domain controller) but have no network rights; network access appears as the computer account. Assign security groups to narrow this; the account then leaves the default admin groups. Event logs show a unique name per session, such as `WinRM Virtual Users\WinRM_VA_1_contoso_alice`.
- gMSA gives a network identity but all users share it, so tracing needs transcripts.
- Pass-through credentials (no run-as) are not recommended: users would need direct privileged group membership and could bypass JEA.
- `RunAsCredential` makes the session not JEA-aware: every authorised user gets the same role, so avoid it.

## WinRM endpoint ACL
The ACL controls who can authenticate; role mapping comes from RoleDefinitions. By default the ACL allows all mapped users. Audit with `Get-PSSessionConfiguration -Name <endpoint> | Select-Object Permission`; change with `Set-PSSessionConfiguration -ShowSecurityDescriptorUI` or `-SecurityDescriptorSddl`. Users need at least Invoke rights. A user with access but no mapped role gets only the default cmdlets.

## JEA does not protect against admins
Domain Admins or local Administrators can bypass JEA (RDP, remote MMC, unconstrained endpoints) and can edit JEA configuration. The page notes just-in-time privileged access systems are commonly used alongside JEA.

## Checked
Method: 2026-11-08 docs-only read of the JEA security-considerations and role-capabilities pages (MicrosoftDocs/PowerShell-Docs markdown). Dropped unsupported items from the old list (New-PSSession, Enter-PSSession, Set-ExecutionPolicy, sc.exe, wmic, msiexec, rundll32, SIEM shipping, red-team step) and the claim that functions run in FullLanguage (the page says default language mode). Unchanged: use explicit parameter limits and a virtual account.
