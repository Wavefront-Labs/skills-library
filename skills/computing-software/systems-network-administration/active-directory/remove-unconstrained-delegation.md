---
id: computing-software.systems-network-administration.active-directory.remove-unconstrained-delegation
name: remove-unconstrained-delegation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, unconstrained-delegation-removal, unconstrained-delegation, resource-based-constrained-delegation]
level: advanced
status: docs-checked
description: "Find computers and users trusted for unconstrained delegation, identify what relies on it, and convert to constrained or resource-based delegation."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-constrained-delegation-overview
  - https://learn.microsoft.com/en-us/defender-for-identity/security-assessment-unconstrained-kerberos
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing unconstrained delegation

A service account or computer trusted for unconstrained delegation can impersonate any client that requests its service, which makes it a high-value target; Microsoft Defender for Identity reports unconstrained delegation as an exposure.

## Find
```powershell
Get-ADComputer -Filter {TrustedForDelegation -eq $true -and PrimaryGroupID -ne 516} -Properties TrustedForDelegation,servicePrincipalName,OperatingSystem |
  Select Name,OperatingSystem
Get-ADUser -Filter {TrustedForDelegation -eq $true} -Properties servicePrincipalName | Select Name,servicePrincipalName
```
Domain controller accounts have primary group ID 516 (Domain Controllers) and are excluded by the filter. Review every other result.

## Find out why it is set
- Usually an old IIS, SharePoint, SSRS or file-print setup that needed double-hop before constrained delegation was
  understood. Ask the owner which back end it calls.
- Check 4624 logon events with `Impersonation Level: Delegation` (SecurityDelegation) on back-end servers to see which front ends delegate.

## Convert
- **RBCD** on the back end (documented across domains; managed by the resource owner):
```powershell
Set-ADComputer SQL01 -PrincipalsAllowedToDelegateToAccount (Get-ADComputer WEB01)
```
- Or constrained delegation on the front end:
```powershell
Set-ADComputer WEB01 -Add @{'msDS-AllowedToDelegateTo'=@('MSSQLSvc/sql01.corp.example.com:1433','MSSQLSvc/sql01.corp.example.com')}
```
- Then remove unconstrained:
```powershell
Set-ADAccountControl WEB01$ -TrustedForDelegation $false
```
The app may need the server restarted or its tickets purged (`klist purge -li 0x3e7`) to pick up the change.

## Compensating controls while it remains
- Mark all admin accounts "Account is sensitive and cannot be delegated" and add them to Protected Users.

## Verify
- [ ] The query returns no computers other than domain controllers.
- [ ] Double-hop app tested with the new delegation type.

## Checked
Checked 2026-10-27 against Microsoft Learn (Kerberos constrained delegation overview; Set-ADComputer, Set-ADAccountControl and Get-ADComputer references, Windows Server 2025; event 4624 reference; Defender for Identity security assessments).
- Confirmed: Set-ADComputer -PrincipalsAllowedToDelegateToAccount; Set-ADAccountControl -TrustedForDelegation; TrustedForDelegation as a Get-ADComputer filter property; primary group ID 516 is Domain Controllers; event 4624 Impersonation Level SecurityDelegation (shown as Delegation); constrained delegation across domains.
- Removed: named coercion techniques, the Print Spooler advice and the claim that RBCD works across forests.

Method: documentation only; no commands were run.
