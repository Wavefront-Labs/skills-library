---
id: computing-software.systems-network-administration.powershell.implicit-remoting-import-pssession
name: implicit-remoting-import-pssession
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, import-pssession, export-pssession, implicit-remoting, proxy-functions]
level: practitioner
status: docs-checked
description: "Use implicit remoting: Import-PSSession brings remote commands into the local session, Export-PSSession saves them as a module; prefixes, clobbering, job support, limits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/import-pssession
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/export-pssession
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit remoting with Import-PSSession / Export-PSSession

Imported commands (cmdlets, functions, aliases) run implicitly in the remote PSSession, but you call them with local syntax;
no `Invoke-Command` needed. Keep the PSSession open: closing it makes the imported commands unavailable.

## Import
```powershell
$S = New-PSSession -ComputerName Server01
Invoke-Command -Session $S { Import-Module TestManagement }
Import-PSSession -Session $S -Module TestManagement -Prefix Remote
```
- Profiles do not run in PSSessions, so load modules with `Invoke-Command` first (as above); to import profile-added commands, run the profile in the session manually.
- Default: imports all commands except those whose names already exist locally. `-AllowClobber` imports them anyway, and imported
  commands can hide aliases, functions and cmdlets and replace functions and variables. `-Prefix Remote` makes `Get-Date` arrive as `Get-RemoteDate`.
- Default `-CommandType` is Cmdlet. `-CommandName` accepts wildcards. If you use `-CommandName`, format data is not imported unless you
  add `-FormatTypeName` (e.g. `*`), and `-FormatTypeName` alone imports no commands.
- Imports go into a temporary module that exists only in the session and is returned as a module object (`Get-Command -Module $M` lists its commands).
  All commands are converted to functions, so precedence rules change (functions beat cmdlets; aliases beat functions). A hidden cmdlet can be called with its qualified name (for example `Microsoft.PowerShell.Utility\Get-Date`).
- Every imported command gains an `-AsJob` parameter; use `Receive-Job`.
- `-Module` takes names without wildcards; `-FullyQualifiedModule` is mutually exclusive with it. Providers and variables are not imported.
- Imported commands share remote-command limits, such as not starting programs with a UI (the page cites Notepad).
- The source session needs `Get-Command`, `Get-FormatData`, `Select-Object` and `Get-Help`.
- Execution policy cannot be Restricted or AllSigned in the local session, because the temporary module contains unsigned script files; the page suggests
  `Set-ExecutionPolicy -Scope Process` for a less restrictive policy.
- `-Certificate` signs the format and `.psm1` files in the temporary module.

## Save as a module (Export-PSSession)
```powershell
$S = New-PSSession -ComputerName Server01
Export-PSSession -Session $S -OutputModule TestCmdlets -Type Cmdlet -CommandName *test* -FormatTypeName *
Remove-PSSession $S
Import-Module TestCmdlets
```
- `-OutputModule` is required; default path is `$HOME\Documents\WindowsPowerShell\Modules`. Existing module files make it fail unless `-Force`.
- Exports into a module without importing into the current session. Default exports everything except names that already exist locally; `-AllowClobber` overrides.
- When the module is imported with the original session closed, it uses any open session to the same computer, otherwise it recreates one.
  Session options (`-SessionOption`, `$PSSessionOption`) are not saved: create a PSSession with the options before importing the module.
- Cannot export providers. Needs remoting configured on the computer.

## Checked
Method: 2026-11-08, read both cited learn.microsoft.com cmdlet pages in full (PowerShell-Docs 7.5 markdown). Rewritten to what the pages state. Removed unsupported claims from the earlier draft: deserialization/method-loss limits, session timeouts, pipeline size advice, Exchange `-ConfigurationName` pattern, the Windows PowerShell compatibility (`-UseWindowsPowerShell`) link, and the Get-DC01ADUser output examples. Not executed.
