---
id: computing-software.systems-network-administration.powershell.windows-powershell-compatibility
name: windows-powershell-compatibility
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, pwsh, windows-powershell-compatibility, usewindowspowershell, implicit-remoting, compatible-psedition, migration-5-to-7]
level: advanced
status: verified
description: "Run Windows PowerShell 5.1 modules and scripts from PowerShell 7: compatibility layer, -UseWindowsPowerShell, breaking changes to check, and dual-edition script patterns."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_windows_powershell_compatibility
  - https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell
  - https://learn.microsoft.com/en-us/powershell/scripting/whats-new/module-compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows PowerShell compatibility from PowerShell 7

## How modules load in PS 7
1. Modules marked `CompatiblePSEditions = 'Core'` (or that just work on .NET) load natively.
2. Modules in the Windows PowerShell system folder (`$env:SystemRoot\System32\WindowsPowerShell\v1.0\Modules`)
   without Core compatibility load through the **Windows compatibility layer**: PS 7 starts a
   hidden `powershell.exe` session named `WinPSCompatSession` and imports proxy commands via
   implicit remoting.
3. Force it for any module: `Import-Module ServerManager -UseWindowsPowerShell`.

```powershell
Get-Module Dism | Select-Object Name, ModuleType, Version   # ModuleType Script = proxied
Get-PSSession -Name WinPSCompatSession
```
On Windows 11 build 26200, PowerShell 7.6.7 imported `ScheduledTasks`, `NetAdapter`, `Storage`, `DnsClient` and `Hyper-V` natively
(ModuleType `Manifest`, `CompatiblePSEditions` Desktop/Core), `Appx` as a Binary module, and `Dism` as a `Script` proxy (a
`WinPSCompatSession` appeared). `Import-Module Microsoft.PowerShell.LocalAccounts -UseWindowsPowerShell` forced a proxy, and
`Get-LocalUser` then returned `PSObject`. Which server modules are native depends on the OS and installed RSAT features; the
ActiveDirectory, DnsServer, DhcpServer, ServerManager and WebAdministration modules are not installed here, so none of them was tested.

## Limits of the compatibility layer
- Output is **deserialised**: no methods, nested objects flattened (`Get-LocalUser` and `Get-WmiObject` results were `PSObject`; `LastBootUpTime`
  from `Get-WmiObject` stayed a DMTF string). Pipe to native PS 7 cmdlets expecting live objects and things break.
- Each module goes into the same single compat session; modules needing different state can conflict.
- Block-list: `PSScheduledJob`, `BestPractices` and `UpdateServices` are denied by default: the `powershell.config.json` in 7.6.7's `$PSHOME`
  contained `"WindowsPowerShellCompatibilityModuleDenyList"` with those three, and `Import-Module PSScheduledJob` failed with
  `is blocked from loading using Windows PowerShell compatibility feature by a 'WindowsPowerShellCompatibilityModuleDenyList'`.
- Turn off implicit compat loading with `DisableImplicitWinCompat` in `powershell.config.json` (the setting is documented in about_PowerShell_Config; not toggled here).

## Breaking changes to scan for when migrating scripts
| 5.1 | PS 7 |
|---|---|
| `Get-WmiObject`, `*-WmiObject` | not in PS 7 itself (absent on Linux/macOS and with the Windows module path stripped); on Windows the compat layer still supplied them as proxies in 7.6.7 (`Get-Command Get-WmiObject` -> `Function`, `Microsoft.PowerShell.Management` 1.0). Use CIM cmdlets |
| default file encoding ANSI/UTF-16 (varies) | UTF-8 without BOM everywhere |
| `Invoke-WebRequest` uses IE engine, `-UseBasicParsing` | always basic parsing; `ParsedHtml` gone (not a property in 7.6.7); 5.1's call without `-UseBasicParsing` failed on this machine |
| `New-WebServiceProxy`, `*-EventLog`, `*-Transaction` | not native; on Windows 7.6.7 `Get-Command` still found them as compat-layer proxy functions. Workflows (`workflow W { }`) are a parse error in 7 |
| `ConvertTo-Json` silently truncates | warns on depth truncation |
| `-Encoding Byte` | `-AsByteStream` (7 rejects `Byte`; 5.1 has no `-AsByteStream`) |
| `Out-File` default UTF-16 LE | UTF-8 |
| ISE | VS Code with the PowerShell extension |

Run PSScriptAnalyzer with `PSUseCompatibleCommands`/`PSUseCompatibleSyntax` targeting both
editions to find these (both rules exist in the PSScriptAnalyzer docs; the analyzer was not run here).

## Scripts that must run on both
```powershell
#Requires -Version 5.1
if ($PSVersionTable.PSEdition -eq 'Core') { $enc = @{ Encoding = 'utf8BOM' } } else { $enc = @{ Encoding = 'UTF8' } }
Set-Content -Path out.csv -Value $text @enc
```
Or call the other edition explicitly for a step that needs it:
`powershell.exe -NoProfile -Command { Import-Module X; Do-Thing }` (script block arguments return
deserialised objects).

## Verify
- [ ] Each script's dependencies are checked with `Get-Module -ListAvailable` under `pwsh`.
- [ ] PSScriptAnalyzer compatibility rules report no issues for the target editions.

## Checked
Ran on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: `Import-Module -PassThru` for nine modules (ModuleType and CompatiblePSEditions), the denied
`PSScheduledJob`, `Get-PSSession` showing `WinPSCompatSession`, the forced `-UseWindowsPowerShell` import and its output type, the config file
contents, `Get-Command` for the "removed" cmdlets (with the normal module path, then with it stripped: absent), `Get-WmiObject` output in 7,
`-Encoding Byte` versus `-AsByteStream`, `ParsedHtml`, the `workflow` keyword, the dual-edition `Encoding` splat (`utf8BOM`/`UTF8` both wrote
EF BB BF), and calling `powershell.exe -Command { ... }` from 7 (deserialised result). Config setting names read from about_PowerShell_Config.
