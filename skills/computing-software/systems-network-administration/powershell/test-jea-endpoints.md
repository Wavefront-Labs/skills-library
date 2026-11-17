---
id: computing-software.systems-network-administration.powershell.test-jea-endpoints
name: test-jea-endpoints
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, get-pssessioncapability, role-capability, audit]
level: practitioner
status: docs-checked
description: "Check what a JEA endpoint exposes with Get-PSSessionConfiguration and Get-PSSessionCapability: endpoints, role mappings, role files, per-user commands, -Full details."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/audit-and-report
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-pssessioncapability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing and auditing JEA endpoints

## Find endpoints and mappings
```powershell
Get-PSSessionConfiguration | Where-Object { $_.SessionType -eq 'RestrictedRemoteServer' }
$jea = Get-PSSessionConfiguration -Name 'JEAMaintenance'
$jea.RoleDefinitions.GetEnumerator() | Select-Object Name, @{ Name = 'Role Capabilities'; Expression = { $_.Value.RoleCapabilities } }
```
The Permission property lists who may connect. The roles and commands they get come from RoleDefinitions in the session configuration file used to register the endpoint.

## Find role capability files
JEA reads `.psrc` files from a `RoleCapabilities` folder inside a module. The audit page gives a function that loops over `Get-Module -ListAvailable`, checks each ModuleBase for a `RoleCapabilities` folder and lists the `*.psrc` files. Its note: result order is not necessarily the order JEA picks when role capabilities share a name.

## Per-user effective commands
```powershell
Get-PSSessionCapability -ConfigurationName 'JEAMaintenance' -Username 'CONTOSO\Alice'
Get-PSSessionCapability -ConfigurationName 'JEAMaintenance' -Username 'CONTOSO\Alice' -Full
```
- Default output is the list of commands the user can run, identical to the user running `Get-Command -CommandType All` in the endpoint.
- `-Full` returns an InitialSessionState object describing the runspace the user would get, including Language Mode, Execution Policy and environment variables.
- The cmdlet is for auditing endpoints that use RoleDefinitions (Windows PowerShell 5.0+).
- Caveat: it may not show extra rights when users are only temporarily in groups through a just-in-time access system. Review the mapping of users to roles.

## Checked
Method: 2026-11-08 docs-only read of the JEA audit-and-report page and Get-PSSessionCapability reference (MicrosoftDocs/PowerShell-Docs markdown). Dropped the Pester and delegated-user connection examples, which the pages do not state. Unchanged: using Get-PSSessionCapability per user.
