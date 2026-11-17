---
id: computing-software.systems-network-administration.powershell.environment-variables-in-powershell
name: environment-variables-in-powershell
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, environment-variables, path, setx]
level: practitioner
status: gated
description: "Read and set environment variables correctly: $env: is process scope, persisting to User or Machine with .NET SetEnvironmentVariable, PATH edits and refresh behaviour."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables
  - https://learn.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables in PowerShell

## Scopes
- `$env:NAME = 'x'` changes the **current process** only (and child processes it starts: a child `cmd` printed it). Gone when
  the session ends. Remove one with `$env:NAME = $null` or `Remove-Item Env:NAME` (both confirmed). Beware
  `[Environment]::SetEnvironmentVariable('NAME', $null)` at process scope: in PowerShell 7.5+ it leaves an EMPTY variable
  (docs note; 7.6.7 confirmed), while Windows PowerShell 5.1 removes it.
- Persistent values live in the registry: User (`HKCU\Environment`) or Machine
  (`HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`).

## Read
```powershell
$env:COMPUTERNAME
Get-ChildItem Env: | Sort Name
[Environment]::GetEnvironmentVariable('PATH','Machine')   # persisted value, not the session's
```

## Set persistently
```powershell
[Environment]::SetEnvironmentVariable('APP_HOME','<DATA_VOLUME>\App','Machine')       # admin required
[Environment]::SetEnvironmentVariable('APP_HOME',$null,'User')             # remove
```
The Machine call, the User removal and the setting examples were not run (they change the registry) (gated: unconfirmed, source is paywalled or blocked). Per the
.NET docs the call broadcasts `WM_SETTINGCHANGE` for User and Machine targets, and recommends keeping persisted values
under 2,048 bytes (hard limit: 32,767 characters).
Running processes do not see the change; new processes started by Explorer do after it handles the broadcast. Services
need a restart; already-open consoles need reopening or a manual refresh (gated: unconfirmed, source is paywalled or blocked).

## PATH safely
```powershell
$machine = [Environment]::GetEnvironmentVariable('PATH','Machine')
if (($machine -split ';') -notcontains '<DATA_VOLUME>\Tools') {
  [Environment]::SetEnvironmentVariable('PATH', ($machine.TrimEnd(';') + ';<DATA_VOLUME>\Tools'), 'Machine') }
$env:PATH = [Environment]::GetEnvironmentVariable('PATH','Machine') + ';' + [Environment]::GetEnvironmentVariable('PATH','User')
```
Avoid `setx PATH "%PATH%;..."`: the Microsoft setx page says `%PATH%` is expanded and assigned directly, and that content over
1024 characters is cropped (and the cropped text is what is applied). Merging the User and Machine values follows from `%PATH%`
being the combined process value.

## Expandable values
The registry value kind of `Path` is ExpandString (REG_EXPAND_SZ) under both HKLM (Machine) and HKCU (User); both were read here.
The claim that the .NET setter writes REG_SZ when the value has no `%` (gated: unconfirmed, source is paywalled or blocked). To keep an expandable type, use
`Set-ItemProperty` on the registry key with `-Type ExpandString`.

## Cross-platform
Names are case-sensitive on Linux/macOS (about_Environment_Variables) but not on Windows (`$env:rv_case` read back via
`$env:RV_CASE`); the PATH separator is `:` there and `;` on Windows (`[IO.Path]::PathSeparator`).

## Verify
- [ ] New session shows the variable; PATH has no duplicates or truncation.

## Checked
Ran in PowerShell 7.6.7 and 5.1: process-scope set, child-process visibility, `Env:` drive, `$null` removal variants,
`[IO.Path]::PathSeparator`, the PATH split/append arithmetic (no write), case-insensitivity on Windows, and read-only
registry value kinds for `Path` in HKLM and HKCU. setx's 1024-character crop was read on the Microsoft Learn setx page;
`WM_SETTINGCHANGE` and the 2,048-byte advice on the .NET Environment.SetEnvironmentVariable reference
(dotnet-api-docs); the 7.5+ empty-value behaviour from about_Environment_Variables and confirmed by run. No persistent
(User/Machine) variable was written because that changes system settings, hence the gated markers.
