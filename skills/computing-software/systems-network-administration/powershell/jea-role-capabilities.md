---
id: computing-software.systems-network-administration.powershell.jea-role-capabilities
name: jea-role-capabilities
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, just-enough-administration, role-capability, psrc, new-psrolecapabilityfile, visiblecmdlets, visiblefunctions, validateset, validatepattern, least-privilege]
level: advanced
status: docs-checked
description: "Write JEA role capability files (.psrc): VisibleCmdlets with constrained parameters, functions, external commands, providers, module placement, and how overlapping roles merge."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/role-capabilities
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/new-psrolecapabilityfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JEA role capability files (.psrc)

A role capability is a PowerShell data file with the `.psrc` extension listing the cmdlets, functions, providers and external programs available to connecting users. `New-PSRoleCapabilityFile -Path .\MyFirstJEARole.psrc` creates a template (the cmdlet was introduced in Windows PowerShell 5.0; the file must end in `.psrc`). Edit it to allow only what the role needs.

## Choose commands
Identify what users run (survey staff, read scripts, analyse transcripts), prefer PowerShell equivalents to command-line tools (external programs cannot be constrained as granularly), restrict parameters and values, wrap hard-to-constrain commands in custom functions, and test with the users. Commands in a JEA session are often run with elevated privileges, so unconstrained commands can be abused. The page's cautionary examples (not exhaustive):
- Granting admin to bypass JEA: `Add-ADGroupMember`, `Add-LocalGroupMember`, `net.exe`, `dsadd.exe`.
- Running arbitrary code: `Start-Process`, `New-Service`, `Invoke-Item`, `Invoke-WmiMethod`, `Invoke-CimMethod`, `Invoke-Expression`, `Invoke-Command`, `New-ScheduledTask`, `Register-ScheduledJob`.

## Visible cmdlets and functions
```powershell
VisibleCmdlets = @('Restart-Computer', 'Get-NetIPAddress')

VisibleCmdlets = @(
    @{ Name = 'Restart-Service'; Parameters = @{ Name = 'Name'; ValidateSet = @('Dns', 'Spooler') } }
    @{ Name = 'Start-Website';   Parameters = @{ Name = 'Name'; ValidatePattern = 'HR_*' } }
)
```
- Use `Get-Command <name>` and check CommandType to decide between VisibleCmdlets and VisibleFunctions.
- Common PowerShell parameters are always allowed; do not list them under Parameters.
- `Name` forms: `'My-Func'`, `'MyModule\My-Func'`, or wildcards (`'My-*'`, `'*-Func'`). The page warns against wildcards; list each trusted command explicitly.
- ValidatePattern and ValidateSet cannot both apply to one cmdlet or function; ValidatePattern overrides ValidateSet.

## External commands and scripts
Add the full path of each program or `.ps1` to `VisibleExternalCommands`. Use full paths so similarly named programs elsewhere do not run. Prefer a cmdlet with limited scope: allowing `net.exe` lets a user run `net group Administrators <user> /add`, whereas `Get-SmbShare` reads shares only.

## Providers
No PowerShell providers are available in JEA sessions by default. `VisibleProviders = 'Registry'` opens one. For simple file, registry or certificate tasks, consider a custom function instead. Commands available in the session are not subject to JEA's provider constraints, which is why the page suggests the user drive for file transfer (see the session configuration skill).

## Custom functions
```powershell
VisibleFunctions = 'Get-TopProcess'
FunctionDefinitions = @{
    Name        = 'Get-TopProcess'
    ScriptBlock = {
        param($Count = 10)
        Get-Process | Sort-Object -Property CPU -Descending |
            Microsoft.PowerShell.Utility\Select-Object -First $Count
    }
}
```
- Add each function name to VisibleFunctions or users cannot run it.
- The function body runs in the system's default language mode, not JEA's constraints, so it can reach the file system and registry and run commands not made visible. Avoid piping user input into `Invoke-Expression`.
- Constrained cmdlets (for example `Select-Object`) keep their constraints inside functions; use the fully qualified module name to get the full implementation.
- For several functions, put them in a script module and expose them with VisibleFunctions.
- For tab completion, include `TabExpansion2` in VisibleFunctions.

## Where JEA finds the file
Before PowerShell 6, the `.psrc` must be in a `RoleCapabilities` folder inside a PowerShell module on `$Env:PSModulePath` (not in `$Env:SystemRoot\System32` or anywhere untrusted users can write). At least one file in the module folder must share the folder's name; the page creates an empty `.psm1` plus a manifest for this. From PowerShell 6, the session configuration file's RoleDefinitions property can point to a role configuration file.

## Updating and merging
- New sessions pick up edits to a `.psrc`. Only highly trusted administrators should change role files; an untrusted user who can edit one can grant themselves privilege-elevating cmdlets. The page advises read-only access for Local System.
- A user in several roles gets the most permissive combination: parameter sets across roles are unioned; an unconstrained role cancels another role's ValidateSet or ValidatePattern; ValidateSets from several roles are unioned; ValidatePatterns accept any match; a ValidateSet is ignored when another role has a ValidatePattern on the same parameter.
- Other fields (external commands, aliases, providers, scripts to process) are simply cumulative. Combining one role's `Remove-Item` with another's FileSystem provider risks arbitrary file deletion.

## Checked
Method: 2026-11-08 docs-only read of the JEA role-capabilities page and New-PSRoleCapabilityFile reference (MicrosoftDocs/PowerShell-Docs markdown). Rewrote to the page; dropped the unsupported "escape hatches" list, the sample .psrc with Invoke-WebRequest, and the verification checklist. Unchanged: restricting parameters via ValidateSet.
