---
id: computing-software.systems-network-administration.powershell.powershell-providers-and-psdrives
name: powershell-providers-and-psdrives
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, psprovider, psdrive, registry-provider]
level: practitioner
status: gated
description: "Navigate data stores with PowerShell providers: FileSystem, Registry, Certificate, Env, WSMan and AD drives, New-PSDrive persistence, and provider-specific parameters."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_providers
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-psdrive
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell providers and PSDrives

Providers expose data stores as drives so the same `*-Item`, `*-ChildItem`, `*-ItemProperty` cmdlets work everywhere.

## Built-in providers and drives
```powershell
Get-PSProvider
Get-PSDrive
```
| Provider | Drives | Typical use |
|---|---|---|
| FileSystem | C:, D:, \\server\share paths | files |
| Registry | HKLM:, HKCU: | `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion` |
| Certificate | Cert: | `Get-ChildItem Cert:\LocalMachine\My -ExpiringInDays 30` (ran; 0 matches) |
| Environment | Env: | `$env:PATH`, `Get-ChildItem Env:` |
| WSMan | WSMan: | WinRM configuration (`Get-Item WSMan:\localhost\MaxEnvelopeSizekb`) (gated: unconfirmed, source is paywalled or blocked); on the test machine `WSMan:\localhost\...` did not exist because WinRM was not running |
| Alias, Function, Variable | Alias:, Function:, Variable: | session contents |
| ActiveDirectory (module) | AD: | `Get-Acl "AD:\OU=Corp,DC=corp,DC=example,DC=com"` (gated: unconfirmed, source is paywalled or blocked) (RSAT module absent here) |

## Registry specifics
- Keys are items, values are **item properties**:
```powershell
New-Item -Path HKLM:\SOFTWARE\Contoso -Force
New-ItemProperty -Path HKLM:\SOFTWARE\Contoso -Name Mode -Value 2 -PropertyType DWord -Force
Get-ItemPropertyValue HKLM:\SOFTWARE\Contoso -Name Mode
```
- HKCR, HKU are not mapped by default (`Get-PSProvider` listed only `HKLM` and `HKCU` for Registry):
  `New-PSDrive -Name HKU -PSProvider Registry -Root HKEY_USERS` created the drive.
- The three registry-writing commands above were not run (HKLM writes change system settings) (gated: unconfirmed, source is paywalled or blocked); `Get-ItemProperty` and
  `Get-ItemPropertyValue` on `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion` ran (`ProductName`, `CurrentBuild`).

## New-PSDrive
```powershell
New-PSDrive -Name Reports -PSProvider FileSystem -Root \\fs01\reports -Credential CORP\me
New-PSDrive -Name R -PSProvider FileSystem -Root \\fs01\reports -Persist     # real mapped drive letter visible in Explorer
```
Without `-Persist` the drive exists only in the session; created inside a script it vanished when the script returned unless `-Scope Global`
was given (tested: a script-scope drive was gone afterwards, a `-Scope Global` one remained). A local-folder `New-PSDrive -Root` ran; the
UNC, `-Credential` and `-Persist` forms were not run (`-Persist` maps a real drive letter) (gated: unconfirmed, source is paywalled or blocked).

## Dynamic parameters
Providers add parameters: `Get-ChildItem -File -Recurse` (FileSystem), `-CodeSigningCert`/`-ExpiringInDays`
(Certificate; both appear only when the current location or `-Path` is under `Cert:`), `-Encoding`/`-Stream` on file content cmdlets
(all confirmed in `Get-Command` output).

## Literal paths
Square brackets are wildcards in provider paths; use `-LiteralPath` for files like `report[1].txt` (the wildcard form found 0 files,
`-LiteralPath` found 1).

## Verify
- [ ] Scripts use provider paths consistently and `-LiteralPath` where names may contain wildcards.

## Checked
Ran on PowerShell 7.6.7 and 5.1.26100: `Get-PSProvider`/`Get-PSDrive`, `Cert:` query with `-ExpiringInDays`, the WSMan path (absent: WinRM not running),
`New-PSDrive` for HKU and for a local folder, script-scope versus `-Scope Global` drive lifetime, registry reads, `Env:`, `Get-Acl`
on a folder, the provider-added parameters via `Get-Command` (including under `Cert:`), and the bracket-wildcard behaviour. Registry
writes, persistent mapped drives, WSMan and AD paths were not run, so those lines carry the gated marker.
