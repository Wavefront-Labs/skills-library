---
id: computing-software.systems-network-administration.powershell.second-hop-remoting
name: second-hop-remoting
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, second-hop, double-hop, credssp, resource-based-constrained-delegation, rbcd, principalsallowedtodelegatetoaccount, kerberos-delegation, pssessionconfiguration-runas]
level: advanced
status: docs-checked
description: "Solve the PowerShell second hop: why it fails and the documented options (CredSSP, constrained and resource-based delegation, JEA, RunAs, passed credentials) with trade-offs."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/ps-remoting-second-hop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell second hop

**Problem:** from ServerA you remote to ServerB, and a command there touches ServerC. Access is denied because the credentials used to create the session are not passed from ServerB to ServerC.

## Options, in the page's order of preference
| Method | Page's note |
|---|---|
| CredSSP | Balances ease of use and security |
| Resource-based Kerberos constrained delegation | Higher security, simpler configuration |
| Kerberos constrained delegation | High security, needs Domain Administrator |
| Unconstrained delegation | Not recommended; testing only |
| JEA | Can be best security, more detailed configuration |
| PSSessionConfiguration with RunAs | Simpler, but credential management |
| Credentials inside an Invoke-Command script block | Simplest, but you must provide credentials |

## CredSSP
Caches credentials on ServerB, so a compromised ServerB exposes them. Disabled by default on client and server; enable only in the most trusted environments (example: a domain admin connecting to a domain controller). Works on Windows Server 2008 or later but needs client and server roles configured, and does not work with the Protected Users group.

## Resource-based constrained delegation (Windows Server 2012+)
Configure on ServerC (where the resource lives). No stored credentials, configured with cmdlets, no Domain Administrator needed, works across domains and forests. Does not support the second hop for WinRM, and needs rights to update objects and SPNs. Accounts marked "Account is sensitive and can't be delegated" cannot be delegated.
```powershell
Add-WindowsFeature RSAT-AD-PowerShell; Import-Module ActiveDirectory
$ServerB = Get-ADComputer -Identity ServerB
$ServerC = Get-ADComputer -Identity ServerC
Set-ADComputer -Identity $ServerC -PrincipalsAllowedToDelegateToAccount $ServerB   # array allowed; $null removes
Invoke-Command -ComputerName $ServerB.Name -Credential $cred -ScriptBlock { klist purge -li 0x3e7 }
```
- The parameter sets the attribute `msDS-AllowedToActOnBehalfOfOtherIdentity` (an ACL of accounts allowed to delegate to ServerC). WinRM runs as the computer account (NetworkService), hence the ServerB computer object.
- The KDC negative-caches denials for 15 minutes; if ServerB tried ServerC earlier, run the `klist purge` above, restart, or wait.
- Across domains, pass `-Server <FQDN of the domain controller of ServerB's domain>` to `Get-ADComputer`.

## Legacy constrained delegation
Needs "Use any authentication protocol" for protocol transition; requires Domain Administrator, configured on ServerB's AD object, one domain only, no second hop for WinRM.

## JEA and RunAs
- JEA: no password maintenance with a virtual account; needs WMF 5.0+ and configuration on every intermediate server.
- Session configuration on ServerB with `RunAsCredential`: any server with WMF 3.0+, but needs configuration on every intermediate server and password maintenance for a domain RunAs account. (The JEA security page advises against RunAsCredential on JEA endpoints.)

## Credentials in the script block
```powershell
$cred = Get-Credential Contoso\Administrator
Invoke-Command -ComputerName ServerB -Credential $cred -ScriptBlock {
    hostname
    Invoke-Command -ComputerName ServerC -Credential $Using:cred -ScriptBlock { hostname }
}
```
No special server configuration; awkward technique.

## Checked
Method: 2026-11-08 docs-only read of the PS-remoting-second-hop page (MicrosoftDocs/PowerShell-Docs markdown). Corrected the old ordering (the page lists CredSSP first), dropped the claims that RBCD is the top choice, New-PSDrive technique, Enable-WSManCredSSP commands, and klist verification, none of which the page states. Unchanged: the klist purge step.
