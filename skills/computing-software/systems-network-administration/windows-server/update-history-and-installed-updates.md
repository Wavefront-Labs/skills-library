---
id: computing-software.systems-network-administration.windows-server.update-history-and-installed-updates
name: update-history-and-installed-updates
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-updates, servicing, get-hotfix, checkpoint-cumulative-updates, update-failures]
level: practitioner
status: docs-checked
description: "Report installed updates and build numbers across servers: Get-HotFix, UBR registry value and checkpoint cumulative updates."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/update/catalog-checkpoint-cumulative-updates
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update history and installed updates

"Is SRV01 patched?" is best answered by the **build number (UBR)**, not by a KB list.

## Build and revision
```powershell
$cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
"{0}.{1}" -f $cv.CurrentBuild, $cv.UBR          # e.g. 20348.2849
```
Compare against the published build numbers for the OS. Fleet-wide:
```powershell
Invoke-Command -ComputerName (Get-Content servers.txt) {
  $cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
  [pscustomobject]@{Build="$($cv.CurrentBuild).$($cv.UBR)"; Product=$cv.ProductName} } |
  Sort Build | Format-Table PSComputerName,Product,Build
```

## Get-HotFix (Win32_QuickFixEngineering)
```powershell
Get-HotFix -ComputerName SRV01 | Sort InstalledOn -Desc | Select -First 10
```
Get-HotFix uses the Win32_QuickFixEngineering WMI class.

## Checkpoint cumulative updates
Checkpoint cumulative updates change how offline installs are ordered; follow the catalog and checkpoint cumulative updates page for the install sequence.

## Verify
- [ ] Fleet report shows every server at the current month's UBR or a documented exception.

## Checked
2026-10-28: Confirmed on Learn pages get-hotfix and fix-windows-update-errors: Get-HotFix -ComputerName, it uses Win32_QuickFixEngineering, UBR appears in the build listing; checkpoint cumulative updates page exists. Removed: claims about what Get-HotFix misses, the Windows Update COM history script, the DISM package install claim and Server 2025 scope.
Method: documentation only; no commands were run.
