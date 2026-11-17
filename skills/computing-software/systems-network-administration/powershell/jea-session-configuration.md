---
id: computing-software.systems-network-administration.powershell.jea-session-configuration
name: jea-session-configuration
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, just-enough-administration, pssc, new-pssessionconfigurationfile, register-pssessionconfiguration, jea-virtual-account, runasvirtualaccount, groupmanagedserviceaccount, roledefinitions, sessiontype-restrictedremoteserver, jea-role-definitions]
level: advanced
status: docs-checked
description: "Create and register a JEA endpoint: .pssc with RoleDefinitions, virtual account vs gMSA identity, RestrictedRemoteServer defaults, transcripts, user drive, registering."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/session-configurations
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/register-jea
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JEA session configuration (.pssc) and registration

A session configuration file defines who can use the endpoint, which roles they get, which identity JEA uses, and the endpoint name.

```powershell
New-PSSessionConfigurationFile -SessionType RestrictedRemoteServer -Path .\MyJEAEndpoint.pssc   # add -Full for every setting
Test-PSSessionConfigurationFile -Path .\MyJEAEndpoint.pssc     # a file that fails this cannot be registered
Register-PSSessionConfiguration -Path .\MyJEAConfig.pssc -Name 'JEAMaintenance' -Force
```

## RestrictedRemoteServer
Sessions run in NoLanguage mode, with only `Clear-Host`, `Exit-PSSession`, `Get-Command`, `Get-FormatData`, `Get-Help`, `Measure-Object`, `Out-Default`, `Select-Object` (and aliases). No providers or external programs.

## Identity
- `RunAsVirtualAccount = $true`: temporary per-user account. On a member server or workstation it joins local Administrators; on a domain controller, Domain Admins. `RunAsVirtualAccountGroups = 'NetworkOperator','NetworkAuditor'` replaces that (local groups on non-DCs).
- `GroupManagedServiceAccount = 'Domain\MyJEAGMSA'` for network resources. All users share one identity, so tracing needs transcripts and logs; it needs a domain-joined machine with PowerShell 5.1+.
- See the security pitfalls skill for why RunAsCredential is discouraged.

## Roles and access
```powershell
RoleDefinitions = @{
    'CONTOSO\JEA_DNS_ADMINS'    = @{ RoleCapabilities = 'DnsAdmin', 'DnsOperator', 'DnsAuditor' }
    'CONTOSO\JEA_DNS_AUDITORS'  = @{ RoleCapabilities = 'DnsAuditor' }
}
```
- Everyone in RoleDefinitions is granted access to the endpoint. Each user or group may appear as a key once, with several roles. Role names are the `.psrc` base names without extension. A user in several groups gets all of their roles, with the most permissive parameters on overlapping cmdlets.
- For local users or groups use the computer name (`$Env:COMPUTERNAME`), not localhost or wildcards.
- Role capability name collisions are resolved by search order over `$Env:PSModulePath` modules with a `RoleCapabilities` folder, preferring Windows-shipped ones; otherwise file enumeration order, which is not guaranteed. The page strongly recommends unique role file names.
- `RequiredGroups` (PowerShell 5.1+) adds conditional access: `@{ And = 'elevated-jea' }`, `@{ Or = '2FA-logon','smartcard-logon' }`, nestable.

## Transcripts and user drive
- `TranscriptDirectory = '<path>'`; written by Local System, so standard users need no access.
- `MountUserDrive = $true` gives each user a persistent PSDrive folder for copying files without exposing the FileSystem provider. Default maximum 50MB per user; set `UserDriveMaximumSize` (bytes). Clean up nightly with a scheduled task if persistence is unwanted. PowerShell 5.1+.

## Register, update, unregister (register-jea page)
- Registering needs administrator rights and the roles already in a module's `RoleCapabilities` folder. `Register-PSSessionConfiguration` restarts WinRM, ending remoting sessions and in-flight DSC configurations, so take production machines offline first.
- The `.pssc` is not used after registration. Endpoints starting with `microsoft` ship with Windows; `microsoft.powershell` is the default endpoint.
- To change a configuration, `Unregister-PSSessionConfiguration -Name <name> -Force` and register again; unregistering also restarts WinRM, so use maintenance windows.

## Checked
Method: 2026-11-08 docs-only read of the JEA session-configurations and register-jea pages (MicrosoftDocs/PowerShell-Docs markdown). Dropped unsupported detail from the old draft (connection steps and checks not on these pages). Unchanged: SessionType RestrictedRemoteServer and RoleDefinitions syntax.
