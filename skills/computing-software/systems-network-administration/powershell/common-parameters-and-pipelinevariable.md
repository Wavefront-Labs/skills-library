---
id: computing-software.systems-network-administration.powershell.common-parameters-and-pipelinevariable
name: common-parameters-and-pipelinevariable
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, advanced-functions, common-parameters, pipelinevariable, cmdletbinding]
level: practitioner
status: verified
description: "Use the common parameters that CmdletBinding gives every function: Verbose, Debug, ErrorAction, ErrorVariable, OutVariable, WarningAction and PipelineVariable."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common parameters and PipelineVariable

`[CmdletBinding()]` (or any `[Parameter()]` attribute) turns a function into an advanced function and adds the common
parameters automatically. Do not declare them yourself.

## The useful ones
| Parameter | Effect |
|---|---|
| `-Verbose` / `-Debug` | show Write-Verbose / Write-Debug output for this call (propagates to cmdlets called inside) |
| `-ErrorAction Stop|Continue|SilentlyContinue|Ignore` | per-call override of `$ErrorActionPreference` for non-terminating errors |
| `-ErrorVariable err` / `+err` | collect errors in `$err` (prefix `+` to append) without checking `$Error` |
| `-WarningAction`, `-WarningVariable`, `-InformationAction`, `-InformationVariable` | same idea for other streams |
| `-OutVariable out` | store output in a variable and still pass it down the pipeline |
| `-OutBuffer n` | batch objects before passing (rarely needed) |
| `-PipelineVariable pv` | name the current pipeline object so later stages can reach it |
| `-WhatIf` / `-Confirm` | only when `SupportsShouldProcess` is declared |

## PipelineVariable example
```powershell
Get-ChildItem $HOME -Directory -PipelineVariable dir |
  Get-ChildItem -File |
  Select-Object @{n='Dir';e={$dir.Name}}, Name
```
Without it, `$_` in Select-Object refers to the file and the directory is lost. The same shape works for any
parent-then-children pair (for example a group and its members).

## ErrorVariable pattern
```powershell
Get-Item <DATA_VOLUME>\nope, $HOME -ErrorAction SilentlyContinue -ErrorVariable missing
if ($missing) { "Missing: $($missing.TargetObject -join ', ')" }
```

`-WhatIf`/`-Confirm` are absent unless the function declares `SupportsShouldProcess`: calling `-WhatIf` on a plain `[CmdletBinding()]` function fails with "A parameter cannot be found that matches parameter name 'WhatIf'". `-ErrorVariable +err` appends to the existing `$err` (checked: count went 1 to 2). All of this was run on PowerShell 7.6.

## Inside your function
`$PSBoundParameters.ContainsKey('Verbose')` tells you if the caller passed it; `$VerbosePreference` is already set
for you, so plain `Write-Verbose` respects it.

## Verify
- [ ] Functions support `-Verbose` without extra code; no hand-declared `$Verbose` parameters.
