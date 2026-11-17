---
id: computing-software.systems-network-administration.patch-management.windows-installed-update-verification
name: windows-installed-update-verification
category: computing-software
field: systems-network-administration
product: patch-management
tags: [get-hotfix, dism-packages, patch-verification, os-build, cumulative-update, windows]
level: practitioner
status: gated
description: "Verify Windows patch level reliably: OS build and UBR vs the release table, Get-HotFix limits, DISM package state, and querying many servers at once."
sources:
  - https://learn.microsoft.com/en-us/windows/release-health/windows-server-release-info
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix
  - https://learn.microsoft.com/en-us/powershell/module/dism/get-windowspackage
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying installed Windows updates

## Best signal: OS build + UBR
Monthly cumulative updates raise the build revision. Compare with the vendor's release table (Windows release health lists each update's OS build, KB article and date).
```powershell
# registry value names below (gated: unconfirmed, source is paywalled or blocked)
$cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
"{0}.{1}  {2}" -f $cv.CurrentBuild, $cv.UBR, $cv.DisplayVersion
```
UBR ≥ the build of this month's LCU = patched for that cycle (cumulative), regardless of
which KB number the device actually received.

## Get-HotFix (Win32_QuickFixEngineering)
```powershell
Get-HotFix -Id KB5044281 -ComputerName srv01
Get-HotFix | Sort InstalledOn -Desc | Select -First 5
```
`Get-HotFix` takes `-Id` and `-ComputerName`. Its coverage of updates and the reliability of `InstalledOn` dates (gated: unconfirmed, source is paywalled or blocked). Use it as supporting evidence, not as the only truth.

## DISM package state
```powershell
dism /online /get-packages /format:table
Get-WindowsPackage -Online
```
`/Get-Packages` displays basic information about all packages in the image; check the state column for packages that are pending a restart (state names (gated: unconfirmed, source is paywalled or blocked)).

## Many servers
```powershell
Invoke-Command -ComputerName (Get-Content servers.txt) -ScriptBlock {
  $cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
  [pscustomobject]@{ Build = "$($cv.CurrentBuild).$($cv.UBR)"; Product = $cv.ProductName
    }
} | Select PSComputerName, Product, Build | Sort Build | Format-Table
```

## Other components
- .NET Framework: registry `HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full` value `Release` (gated: unconfirmed, source is paywalled or blocked).
- Microsoft 365 Apps and Edge report their versions through their own tools; see the `microsoft-365-apps-update-channels` and `browser-update-policies` skills.

## Verify
Report shows each server's build at or above the cycle's target build and no pending restart (see the `windows-pending-reboot-detection` skill); outliers have tickets.

## Checked

Checked 2026-10-27 against Microsoft Learn: Windows Server release information (release health), Get-HotFix, Get-WindowsPackage and DISM package-servicing options.
- Release health publishes the OS build, KB article and date of each cumulative update (the current Windows Server 2025 table lists builds such as 26100.33674): confirmed.
- `Get-HotFix -Id/-ComputerName`, `Get-WindowsPackage -Online`, `dism /online /get-packages /format:table`: confirmed.
- Registry value names for UBR and the .NET Framework Release value, `Get-HotFix` coverage limits and the DISM package state names could not be confirmed from readable pages; they are marked gated, so the skill is gated.
- Removed unconfirmed: Office and Edge registry locations, the RebootPending registry test.
Method: documentation only; no commands were run.
