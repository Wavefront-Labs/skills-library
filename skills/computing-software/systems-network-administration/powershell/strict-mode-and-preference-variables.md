---
id: computing-software.systems-network-administration.powershell.strict-mode-and-preference-variables
name: strict-mode-and-preference-variables
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, set-strictmode, preference-variables, erroractionpreference, verbosepreference, informationpreference, psnativecommanduseerroractionpreference]
level: practitioner
status: verified
description: "Harden scripts with Set-StrictMode and preference variables: ErrorActionPreference, Verbose/Debug/Information streams, native command errors and scope pitfalls."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-strictmode
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_output_streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set-StrictMode and preference variables

## Script header for automation
```powershell
#Requires -Version 7.2
[CmdletBinding(SupportsShouldProcess)]
param()
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true   # PS 7.4+: non-zero exit codes become errors
```

## Set-StrictMode levels
| Version | Adds |
|---|---|
| `1.0` | error on uninitialised variables (except inside strings: `"a $nov"` passes) |
| `2.0` | + uninitialised variables inside strings, nonexistent properties, function called like a method `f(a,b)` |
| `3.0` / `Latest` | + out-of-bounds or invalid array index |

- Verified on 7.6.7: version 2.0 does not catch `$array[10]`; 3.0 throws "Index was outside the bounds of the array". The level list follows the Set-StrictMode reference.
- Strict mode is **scoped**: it applies to the scope where set and its children, not to
  modules you call. `Set-StrictMode -Off` to disable.
- `Latest` changes meaning with future releases; pin `3.0` in production scripts.
- Common break: `$obj.MaybeMissing` on objects without that property, and `$array[10]`. Test
  with `if ($obj.PSObject.Properties['MaybeMissing'])` or `$obj.psobject.Properties.Name -contains`.

## Preference variables that matter
| Variable | Default | Notes |
|---|---|---|
| `$ErrorActionPreference` | `Continue` | `Stop` makes non-terminating cmdlet errors catchable. Does **not** affect native exe exit codes before 7.4 |
| `$WarningPreference` | `Continue` | |
| `$VerbosePreference` | `SilentlyContinue` | `-Verbose` on a call sets it to `Continue` for that call |
| `$DebugPreference` | `SilentlyContinue` | `-Debug` in PS 7 sets it to `Continue` (5.1: `Inquire`) |
| `$InformationPreference` | `SilentlyContinue` | `Write-Host` writes to stream 6 and is shown regardless |
| `$ProgressPreference` | `Continue` | set `SilentlyContinue` to speed up `Invoke-WebRequest` in 5.1 dramatically (30 MB download: 19.6 s with `Continue`, 0.46 s with `SilentlyContinue` on 5.1.26100; 7.6.7 showed no difference) |
| `$ConfirmPreference` | `High` | prompts when a command's ConfirmImpact >= this |
| `$WhatIfPreference` | `$false` | `$true` makes ShouldProcess commands dry-run |
| `$PSNativeCommandUseErrorActionPreference` | `$false` | 7.4+: treat non-zero exit as error |

## Pitfalls
- Preference variables are **dynamically scoped**: setting one in a script affects every
  function it calls, but cmdlets in **script modules** read the module's scope, so
  `$ErrorActionPreference = 'Stop'` set inside your function or script scope does not reach module functions (checked: the module's `Get-Item` error was displayed and `"mod continued"` ran on 5.1 and 7.6). Set at the global scope it does reach them. Pass
  `-ErrorAction Stop` explicitly when it matters.
- `-ErrorAction Ignore` does not record in `$Error`; `SilentlyContinue` does (checked: counts 0 and 1).
- `-Debug` sets `$DebugPreference` to `Continue` on 7.6.7 and `Inquire` on 5.1 (checked).
- With `$PSNativeCommandUseErrorActionPreference = $true` and `Stop`, `cmd /c exit 3` throws "ended with non-zero exit code: 3" on 7.6.7; without it `$LASTEXITCODE` is 3 and nothing throws.
- `$ErrorActionPreference = 'Stop'` turns `Write-Error` in your own functions into terminating
  errors; design for it.
- Native commands: check `$LASTEXITCODE` after every exe on 5.1 and PS < 7.4:
  `robocopy ...; if ($LASTEXITCODE -ge 8) { throw "robocopy failed $LASTEXITCODE" }`
  (robocopy uses 0-7 for success variants, which is why blanket exit-code-as-error needs care).

## Verify
- [ ] A typo'd variable name in a test copy of the script now throws.
- [ ] A failing cmdlet inside `try` reaches `catch` without per-call `-ErrorAction Stop`.
