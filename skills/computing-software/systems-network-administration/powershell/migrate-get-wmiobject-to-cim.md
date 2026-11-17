---
id: computing-software.systems-network-administration.powershell.migrate-get-wmiobject-to-cim
name: migrate-get-wmiobject-to-cim
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-cim, wmi-to-cim-migration, get-ciminstance, get-wmiobject, powershell-7]
level: practitioner
status: verified
description: "Migrate scripts from Get-WmiObject and other WMI cmdlets (removed in PowerShell 7) to CIM cmdlets: equivalents, method calls, sessions, and object differences."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/07-working-with-wmi
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate from Get-WmiObject to CIM cmdlets

The `*-WmiObject` cmdlets use DCOM and are not part of PowerShell 7. On Windows, 7.6.7 still resolved `Get-WmiObject` through the
Windows PowerShell compatibility layer (a `Microsoft.PowerShell.Management` proxy function in a hidden `WinPSCompatSession`): it ran,
but returned deserialised objects whose `LastBootUpTime` is still a DMTF string (`20261018085420.500000+600`), with no
`ConvertToDateTime()`, and on Linux/macOS it does not exist. Do not read "it ran in pwsh" as "migrated". CIM cmdlets use WS-Man (or DCOM via
session options) and work natively in both 5.1 and 7.

## Equivalents
| WMI (5.1 only) | CIM |
|---|---|
| `Get-WmiObject Win32_Service -ComputerName S1` | `Get-CimInstance Win32_Service -ComputerName S1` |
| `Get-WmiObject -Query "SELECT ..."` | `Get-CimInstance -Query "SELECT ..."` |
| `-Filter "Name='x'"` | same `-Filter` (WQL) |
| `(Get-WmiObject Win32_Service -Filter "Name='x'").StopService()` | `Get-CimInstance ... \| Invoke-CimMethod -MethodName StopService` |
| `Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe'` | `Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='notepad.exe'}` |
| `Set-WmiInstance` | `Set-CimInstance` |
| `Remove-WmiObject` | `Remove-CimInstance` |
| `Register-WmiEvent` | `Register-CimIndicationEvent` |
| `[wmi]`, `[wmiclass]` accelerators (still listed in both editions' TypeAccelerators) | `Get-CimInstance` / `Get-CimClass` |

## Differences that break scripts
- CIM objects have **no methods**; call methods with `Invoke-CimMethod` and named argument hashtables.
- Dates are `DateTime` already (no `ConvertToDateTime()`).
- Remote: CIM needs WinRM; for old hosts without it,
  `New-CimSession -SessionOption (New-CimSessionOption -Protocol Dcom)`.
- `__SERVER` etc. system properties: use `CimSystemProperties` (`.ServerName` returned the machine name, `.Namespace`,
  `.ClassName`); `PSComputerName` was empty on local queries and is filled for remote ones.
- `-Credential` is on `New-CimSession`, not on `Get-CimInstance`.

## Find old usage
```powershell
Get-ChildItem -Recurse -Include *.ps1,*.psm1 | Select-String -Pattern 'Get-WmiObject|gwmi |Invoke-WmiMethod|\[wmi(class)?\]'
```
PSScriptAnalyzer's `AvoidUsingWMICmdlet` rule (always enabled, severity Warning per its docs page) flags them too. Note that
`Select-String` without `-AllMatches` reports only the first match on a line.

## Verify
- [ ] Converted scripts run in `pwsh` and `powershell.exe` with identical output.

## Checked
Ran on 7.6.7 and 5.1.26100: `Get-WmiObject` resolution and output in 7 (PSObject, string `LastBootUpTime`), 5.1 `Get-WmiObject` with
`ConvertToDateTime` and `__SERVER`, `Invoke-WmiMethod ... -ArgumentList` versus `Invoke-CimMethod ... -Arguments` (both returned 0 in 5.1),
`CimSystemProperties` fields, TypeAccelerators for `wmi`/`wmiclass`, the `Select-String` scan over sample files, and the absence of
instance methods on CIM objects (earlier CIM run). The cmdlet names in the table were confirmed with `Get-Command` in both editions (all exist in 5.1; in 7.6.7 the `*-Wmi*` names were present too, as
compatibility-layer proxies), but no event subscription or instance edit was run. The PSScriptAnalyzer rule page was read on GitHub (PSScriptAnalyzer docs/Rules).
