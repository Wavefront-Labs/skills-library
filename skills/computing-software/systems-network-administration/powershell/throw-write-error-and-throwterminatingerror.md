---
id: computing-software.systems-network-administration.powershell.throw-write-error-and-throwterminatingerror
name: throw-write-error-and-throwterminatingerror
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, throwterminatingerror, write-error, terminating-errors]
level: advanced
status: verified
description: "Raise errors properly in functions: throw vs Write-Error vs $PSCmdlet.WriteError and ThrowTerminatingError, ErrorRecord construction and caller-friendly errors."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_throw
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# throw, Write-Error and ThrowTerminatingError

## Choose the right one
| Mechanism | Type | Use when |
|---|---|---|
| `Write-Error` / `$PSCmdlet.WriteError()` | non-terminating | one item in a pipeline failed, keep processing others |
| `throw` | script-terminating | the function cannot continue at all; stops the whole script unless caught |
| `$PSCmdlet.ThrowTerminatingError()` | statement-terminating | like a compiled cmdlet's terminating error: stops this command, error points at the caller's line |

## Write-Error with useful metadata
```powershell
Write-Error -Message "Server $name unreachable" -Category ConnectionError -TargetObject $name -ErrorId 'ServerUnreachable'
```
Callers can filter on `$_.FullyQualifiedErrorId` and `$_.CategoryInfo.Category`.

## throw
```powershell
if (-not (Test-Path $Path)) { throw [System.IO.FileNotFoundException]::new("Config not found: $Path") }
```
Throwing a typed exception lets callers `catch [System.IO.FileNotFoundException]`. `throw "text"` creates a
RuntimeException.
Inside `try`/`catch` a `throw` is always caught, whatever `-ErrorAction` the caller passed. Outside a `try`, calling a function with `-ErrorAction SilentlyContinue` suppressed the `throw` message and the function carried on with the next statement (checked on 5.1 and 7.6.7: the line after `throw` ran), which surprises callers who assumed a throw always stops the function.

## ThrowTerminatingError (advanced functions)
```powershell
$ex  = [System.ArgumentException]::new("Unsupported mode '$Mode'")
$rec = [System.Management.Automation.ErrorRecord]::new($ex, 'UnsupportedMode', 'InvalidArgument', $Mode)
$PSCmdlet.ThrowTerminatingError($rec)
```
The error message references the caller's invocation rather than the internals of your function, which reads better.

## Rethrowing
Inside `catch`, `throw` with no argument rethrows the original error preserving its record. Wrapping: `throw
[System.Exception]::new('Context', $_.Exception)` keeps the inner exception.

Run on 5.1 and 7.6.7: `Write-Error` with `-Category`/`-ErrorId` populating `FullyQualifiedErrorId` (`ServerUnreachable,F3`) while the pipeline kept other items, a typed `throw` caught by type, `throw 'text'` giving a `RuntimeException`, wrapping with `[System.Exception]::new('Context', $_.Exception)`, and `ThrowTerminatingError` reporting `F2` as the command with message `bad`.

## Verify
- [ ] Pipeline input with one bad item yields one error and other results; fatal cases stop with a typed error.
