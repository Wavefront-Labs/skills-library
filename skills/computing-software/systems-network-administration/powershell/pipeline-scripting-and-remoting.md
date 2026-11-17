---
id: computing-software.systems-network-administration.powershell.pipeline-scripting-and-remoting
name: pipeline-scripting-and-remoting
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, pwsh, windows-powershell, powershell-7, powershell-5-1, pipeline, objects, where-object, select-object, foreach-object, cmdletbinding, whatif, supportsshouldprocess, try-catch, erroraction, invoke-command, pssession, winrm, ps-remoting, ssh-remoting, executionpolicy, advanced-functions, scripting, automation, windows-server]
level: practitioner
status: draft
description: "PowerShell admin scripting: object pipeline, CmdletBinding with -WhatIf, try/catch with -ErrorAction Stop, Invoke-Command over WinRM/SSH, PS 7 vs 5.1."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/overview
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/running-remote-commands
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PowerShell pipeline scripting and remoting — objects in, objects out, safely at scale

**Goal:** write admin functions that pass objects (not text), support `-WhatIf`, stop
on real errors, and run the same code across many servers.

## 1. Think in objects
Commands emit .NET objects with properties. Filter early, format last.
```powershell
Get-Service | Where-Object Status -eq 'Stopped' | Select-Object Name, StartType
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 Name, Id,
  @{n='MemMB'; e={[math]::Round($_.WorkingSet64/1MB)}}
Get-ChildItem <DATA_DIR> -Recurse -File |
  Where-Object LastWriteTime -lt (Get-Date).AddDays(-90) |
  Measure-Object Length -Sum
```
- Discover properties with `Get-Member` (`gm`) and `Select-Object *`.
- **Filter left:** `Get-ADUser -Filter "Department -eq 'HR'"` or
  `Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008}` is far faster than piping
  everything into `Where-Object`.
- `Format-Table`/`Format-List` produce formatting objects; never pipe them onward. Export
  with `Export-Csv -NoTypeInformation` or `ConvertTo-Json -Depth 5` (default depth is 2,
  silently truncating nested objects).
- `ForEach-Object` streams; `foreach ($x in $list)` is faster on in-memory collections.
  PS 7 adds `ForEach-Object -Parallel -ThrottleLimit 8`.

## 2. Advanced functions
```powershell
function Remove-OldLog {
  [CmdletBinding(SupportsShouldProcess, ConfirmImpact='Medium')]
  param(
    [Parameter(Mandatory, ValueFromPipeline)][string[]]$Path,
    [ValidateRange(1,3650)][int]$Days = 30
  )
  process {
    foreach ($p in $Path) {
      Get-ChildItem -Path $p -File -Filter *.log |
        Where-Object LastWriteTime -lt (Get-Date).AddDays(-$Days) |
        ForEach-Object {
          if ($PSCmdlet.ShouldProcess($_.FullName, 'Delete')) {
            Remove-Item -LiteralPath $_.FullName -ErrorAction Stop
          }
        }
    }
  }
}
Remove-OldLog -Path <LOG_DIR> -Days 14 -WhatIf
```
`CmdletBinding` gives `-Verbose`, `-ErrorAction`, `-WhatIf`/`-Confirm` for free. Use
`Write-Verbose` for chatter and `Write-Output` (or just emit) for data; `Write-Host`
goes to the information stream, not the pipeline, so callers cannot consume it as data.

## 3. Errors that actually stop
Most cmdlet errors are **non-terminating**: `try/catch` will not catch them unless you
force it.
```powershell
try {
  Get-Item -Path <PATH> -ErrorAction Stop
  Restart-Service -Name Spooler -ErrorAction Stop
} catch [System.Management.Automation.ItemNotFoundException] {
  Write-Warning "Missing: $($_.TargetObject)"
} catch {
  Write-Error "Failed: $($_.Exception.Message)"; throw
}
```
Set `$ErrorActionPreference = 'Stop'` at the top of scripts to make this the default.
Native executables (`robocopy`, `git`) do not throw: check `$LASTEXITCODE` (robocopy
codes 0–7 are success). Add `Set-StrictMode -Version Latest` to catch typos in variable
names.

## 4. Remoting
```powershell
$servers = Get-Content .\servers.txt
Invoke-Command -ComputerName $servers -ThrottleLimit 32 -ScriptBlock {
  Get-CimInstance Win32_OperatingSystem | Select-Object CSName, LastBootUpTime
} | Select-Object CSName, LastBootUpTime, PSComputerName

$s = New-PSSession -ComputerName <SERVER>     # reuse for several calls
Invoke-Command -Session $s -ScriptBlock { param($d) Get-ChildItem $d } -ArgumentList '<REMOTE_DIR>'
Remove-PSSession $s
```
- Local variables are not visible remotely: pass with `-ArgumentList` or `$using:var`.
- **WinRM** (HTTP 5985 / HTTPS 5986) is on by default for domain-joined Windows Server.
  Kerberos needs the hostname, not the IP; IP or workgroup targets need HTTPS or
  `TrustedHosts`, and `TrustedHosts` should never be `*` in production.
- The **double hop**: a remote session cannot use your credentials to reach a third
  machine (file share, SQL). Use resource-based Kerberos constrained delegation or pass
  explicit credentials; avoid CredSSP.
- **SSH remoting** (PS 7): `Invoke-Command -HostName <HOST> -UserName admin -ScriptBlock {...}`
  works to Linux and Windows with OpenSSH and a `pwsh` subsystem configured in `sshd_config`.
- Results come back deserialised (property bags, no methods).

## 5. PS 7 vs Windows PowerShell 5.1
5.1 (`powershell.exe`) ships in Windows and is frozen; 7.x (`pwsh.exe`) is
cross-platform, side-by-side, and where new features land (ternary, `??`, `-Parallel`,
`&&`/`||`). Most Windows modules work in 7; a few still need 5.1 (via the Windows
compatibility layer, `Import-Module -UseWindowsPowerShell`). Target 7 for new scripts
and test on 5.1 if they must run on stock servers. Check `$PSVersionTable`.

## 6. Execution policy
Execution policy is a safety catch, not a security boundary (`-ExecutionPolicy Bypass`
skips it). Use `RemoteSigned` broadly; `AllSigned` with code-signing in locked-down
estates. Downloaded scripts carry Mark-of-the-Web: `Unblock-File` after review. Real
controls are App Control for Business / AppLocker, Constrained Language Mode and script
block logging.

## Verify
- [ ] Functions emit objects you can pipe to `Export-Csv` without `Format-*`.
- [ ] Every destructive function supports `-WhatIf` and was run with it first.
- [ ] A forced failure is caught by `catch` (because of `-ErrorAction Stop`).
- [ ] `Invoke-Command` against two test servers returns `PSComputerName` per result.
- [ ] Script runs under the PowerShell version(s) your servers actually have.
