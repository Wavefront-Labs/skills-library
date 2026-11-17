---
id: computing-software.systems-network-administration.patch-management.diagnosing-failed-windows-update-installs
name: diagnosing-failed-windows-update-installs
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-verification, failed-update-install, windowsupdate-log, cbs-log, dism-restorehealth, sfc, component-store, 0x800f0922, windows-update, patch-management]
level: practitioner
status: docs-checked
description: "Fix failed Windows update installs: Get-WindowsUpdateLog, CBS log, documented error codes, DISM RestoreHealth with a source, and manual package install limits."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/common-windows-update-errors
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image
  - https://learn.microsoft.com/en-us/windows/deployment/update/windows-update-logs
  - https://learn.microsoft.com/en-us/powershell/module/windowsupdate/get-windowsupdatelog
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-hotfix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing failed Windows update installs

**Goal:** get a stuck or failing server patched, with evidence of the root cause, instead
of retrying forever.

## Collect
```powershell
Get-WindowsUpdateLog -LogPath "$env:TEMP\WindowsUpdate.log"   # merges the ETW .etl files into one readable log
Get-Content "$env:SystemRoot\Logs\CBS\CBS.log" -Tail 300      # servicing stack (installation) errors
```
Windows Update no longer writes a WindowsUpdate.log directly; `Get-WindowsUpdateLog` produces a static copy that is not
updated until you run it again. `CBS.log` (under `%systemroot%\Logs\CBS`) shows the update installation part of the
servicing stack. Find the KB, the error code (0x8...) and the failing component in CBS.log.

## Common errors (from the Microsoft common-errors table)
| Code | Meaning on the page | Documented mitigation |
|---|---|---|
| 0x800f081f (CBS_E_SOURCE_MISSING), 0x800f0831 (CBS_E_STORE_CORRUPTION), 0x80070570, 0x80073701, 0x8007371b, 0x800f0825 | Component store corruption or a partially installed component | `Dism.exe /Online /Cleanup-Image /Restorehealth`, then `Sfc.exe /Scannow`, then restart |
| 0x800f0922 (CBS_E_INSTALLERS_FAILED) | The page's case: a July cumulative update failing on Windows Server 2016 when license and product key tokens fail to update | Add write permission for the "User" and "Network Service" accounts on the `%SystemRoot%\System32\spp` folder |
| 0x800f0821 / 0x800f0920 | CBS watchdog timeout or hang detected | Give the device more resources (more vCPU and memory on a VM) and make sure KB4493473 or later is installed |
| 0x80070005 | Access denied: permissions on a file or registry key changed | Find the error in the latest CBS.log, work out which object was denied, correct its permissions |
| 0x80070020 | Sharing violation, often non-Microsoft filter drivers such as antivirus | Clean restart and retry; if it persists use Process Monitor plus CBS.log to find the file and the process holding it |
| 0x80070bc9 | The TrustedInstaller startup type was set to Manual by a GPO, leaving a pending transaction that blocks later updates | Set the policy to Automatic and restart; otherwise revert pending actions from WinRE (`dism /Image:<Windows_drive>:\ /Cleanup-Image /RevertPendingActions`) |
| 0x80244022 (HTTP 503), 0x8024401B (HTTP 407) | Cannot reach the update source or proxy needs authentication | Check proxy and network path to the update source |
| 0x80242014 | Post-restart operation still pending | Restart the device |
| 0x80240020 | No interactive user signed in | Sign in and let the device restart |

## Repair
```powershell
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-Image /RestoreHealth /Source:<path_to_mounted_image_or_folder> /LimitAccess
sfc /scannow
```
`/ScanHealth` takes several minutes; `/CheckHealth` reports healthy, repairable or non-repairable (discard a non-repairable
image). Without `/Source`, the Features on Demand repair source (set by Group Policy) is used. `/LimitAccess` stops DISM
using Windows Update as a repair source. Use files from a matching OS build when the server cannot reach Windows Update.

For error 0x80242006 (invalid update metadata) Microsoft's mitigation is to rename these folders and download again:
`%systemroot%\SoftwareDistribution\DataStore`, `%systemroot%\SoftwareDistribution\Download` and
`%systemroot%\system32\catroot2` (for example to `.bak`).

## Manual install
Download the update from the Microsoft Update Catalog. `DISM /Online /Add-Package /PackagePath:<file>.msu` works online
only on Windows 11 version 21H2 or later; on earlier Windows, DISM can add `.msu` packages only to offline images.
`/Add-Package` does not do a full dependency check, so read the KB for package-specific instructions and install any
prerequisites first.

## Gotchas
- A pending restart from a previous update can block new installs (0x80242014, 0x80070bc9): restart first.
- Non-Microsoft filter drivers such as antivirus cause sharing violations (0x80070020) and can block access to folders such as SoftwareDistribution (0x80240022).
- `DISM /Cleanup-Image /StartComponentCleanup` cleans superseded components; with `/ResetBase`, installed updates cannot then be uninstalled.

## Verify
`Get-HotFix -Id <KB>` shows the update installed (`InstalledOn` gives the date); the next scan reports compliant.

## Checked
Date: 2026-11-07. Read in full: Windows Update common errors (every error row), Repair a Windows Image, Windows Update log files, Get-WindowsUpdateLog (syntax and description), DISM operating system package servicing options (Add-Package notes and Cleanup-Image syntax; read the sections, not the whole page), Get-HotFix (searched for `-Id` and `InstalledOn`, not read end to end). Corrected: 0x800f0922 on the page is the Windows Server 2016 `spp` folder permission case, not a System Reserved partition or SSU issue; 0x80244022 means HTTP 503 (draft listed 0x8024402c, not on the page); `.msu` through `DISM /Online /Add-Package` is limited to Windows 11 21H2 or later. Removed as unconfirmed: 0x80073712, 0x800705b4, the `/Source:wim:` syntax, the Microsoft-Windows-WindowsUpdateClient/Operational log query, DISM log path, event 19, `wusa.exe` command line (its Learn page returned 404), and the service-stop/rename reset recipe.
Method: documentation only; no commands were run.
