---
id: computing-software.systems-network-administration.powershell.function-output-streams-and-outputtype
name: function-output-streams-and-outputtype
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, advanced-functions, outputtype, output-streams, write-output]
level: practitioner
status: verified
description: "Control what PowerShell functions return: every uncaptured value is output, suppressing noise with $null, the six streams, redirection and [OutputType]."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_output_streams
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_outputtypeattribute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function output streams and OutputType

## Everything uncaptured is output
```powershell
function Get-Thing {
  $list = [System.Collections.ArrayList]::new()
  $list.Add('a')            # BUG: Add returns the index (0), which becomes output
  New-Item -ItemType Directory $env:TEMP\x   # BUG: DirectoryInfo becomes output
  return 'done'
}
(Get-Thing).Count   # 3, not 1
```
Suppress: `$null = $list.Add('a')`, `[void]$list.Add('a')`, or `| Out-Null` (slowest). `return` does not mean "only
this"; it adds its value and exits.

## The streams
| # | Stream | Write with | Preference variable |
|---|---|---|---|
| 1 | Success/output | `Write-Output` or bare value | |
| 2 | Error | `Write-Error` | `$ErrorActionPreference` |
| 3 | Warning | `Write-Warning` | `$WarningPreference` |
| 4 | Verbose | `Write-Verbose` | `$VerbosePreference` (or `-Verbose`) |
| 5 | Debug | `Write-Debug` | `$DebugPreference` |
| 6 | Information | `Write-Information`, `Write-Host` (5.0+) | `$InformationPreference` |

Diagnostic messages go to 3-6, never to output, so callers get clean objects.

## Redirection
```powershell
Get-Thing 2>errors.txt 3>&1 *>all.txt   # redirections apply left to right; later ones can take streams from earlier ones, so check both files
$out = Get-Thing 6>$null            # drop Write-Host/Information
$all = Get-Thing *>&1               # merge everything into output (records keep their type)
```

## [OutputType]
```powershell
function Get-DiskReport {
  [CmdletBinding()]
  [OutputType([pscustomobject])]
  param()
  Get-CimInstance Win32_LogicalDisk | ForEach-Object { [pscustomobject]@{Drive=$_.DeviceID; FreeGB=[math]::Round($_.FreeSpace/1GB,1)} }
}
```
Purely documentation for help and tab completion; PowerShell does not enforce it.

## Arrays unrolling
Returning an array unrolls it in the pipeline; a single-element array becomes a scalar to the caller. Use
`Write-Output -NoEnumerate $arr` or `,$arr` when the caller must receive the collection as one object.

Run on 7.6.7: `(Get-Thing).Count` is 3; `*>&1` yields `String`, `ErrorRecord`, `WarningRecord`, `VerboseRecord` and `InformationRecord` objects (Write-Host and Write-Information are both `InformationRecord`); `6>$null` removes the Write-Host line; `[OutputType([int])]` on a function that returns a string still returns a `String` while `(Get-Command f).OutputType` reports `Int32`; `return @(1)` arrives as an `Int32`, whereas `Write-Output -NoEnumerate` and `,$a` keep an `Object[]`.

## Verify
- [ ] `Get-Thing | Get-Member` shows only intended types.
