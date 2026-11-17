---
id: computing-software.it-support-helpdesk.intune-mdm.resetting-windows-update-components
name: resetting-windows-update-components
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, reset-windows-update, softwaredistribution, catroot2, dism-restorehealth, sfc, windows-update-troubleshooting, windowsupdate-log]
level: practitioner
status: docs-checked
description: "Repair a Windows client whose updates keep failing: read the logs, DISM and SFC repair, reset the Windows Update components (SoftwareDistribution, catroot2), escalation order."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/additional-resources-for-windows-update"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image"
  - "https://learn.microsoft.com/en-us/powershell/module/windowsupdate/get-windowsupdatelog"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# resetting-windows-update-components

Do the cheap diagnosis first; a reset is the last resort ("if all else fails" in Microsoft's wording).

## 1. Read the logs
- Settings > Windows Update > Update history for the KB and error code.
- Windows Update no longer writes `WindowsUpdate.log` directly; it writes .etl trace files. `Get-WindowsUpdateLog` merges
  them into a readable `WindowsUpdate.log`, by default on the current user's Desktop (`-LogPath` changes it).
  `-IncludeAllLogs` also decodes the Update Session Orchestrator (USO.log) and UX logs into a folder on the desktop.
  For Windows 10 1709 and later logs, decode on 1709 or later; no symbol server is needed.
- `-ForceFlush` flushes traces to .etl files but stops the Update Orchestrator and Windows Update services, and needs an
  elevated session.

## 2. Try the built-in fixes first
Microsoft's order: the Windows Update Troubleshooter (analyses and resets components that need it), then its Windows
Update troubleshooting and "Fix Windows Update errors" articles.

## 3. Repair the component store
```cmd
Dism /Online /Cleanup-Image /ScanHealth
Dism /Online /Cleanup-Image /CheckHealth
Dism /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```
`/CheckHealth` reports whether the image is healthy, repairable or non-repairable. Use `/RestoreHealth` if repairable.
With no `/Source`, the repair source is the one used for Features on Demand, determined by Group Policy. To use your own
files instead of Windows Update, add `/Source:<path> /LimitAccess`; `/LimitAccess` stops DISM using Windows Update as a
primary or backup source. With several `/Source` values, files come from the first location that has them. `sfc /scannow`
is the quick check for an online image.

## 4. Reset the update components manually (elevated)
Microsoft's short form, when all else fails:
```cmd
net stop wuauserv
rd /s /q %systemroot%\SoftwareDistribution
net start wuauserv
```
The fuller manual procedure:
```cmd
net stop bits
net stop wuauserv
net stop cryptsvc
Del "%ALLUSERSPROFILE%\Application Data\Microsoft\Network\Downloader\qmgr*.dat"
Ren %Systemroot%\SoftwareDistribution\DataStore DataStore.bak
Ren %Systemroot%\SoftwareDistribution\Download Download.bak
Ren %Systemroot%\System32\catroot2 catroot2.bak
net start bits
net start wuauserv
net start cryptsvc
```
Microsoft says to skip the three `Ren` lines on a first attempt and only do them if the issue persists. The same page
adds, as later steps: resetting the BITS and Windows Update service security descriptors with `sc.exe sdset` (this
overwrites the existing ACLs with defaults, so skip it unless the other steps failed), re-registering a long list of DLLs
with `regsvr32.exe`, and `netsh winsock reset`. Read the page for the exact lists rather than copying from memory.

## Gotchas
- This article is a Windows client troubleshooting aid; the Intune update report is separate and may lag the device.
- For support escalation, Microsoft points to collecting data with TSS (deployment-related issues).

## Verify
The KB installs and Update history shows it, and `Dism /Online /Cleanup-Image /ScanHealth` reports no corruption.

## Checked
Date: 2026-11-08. Read in full: Learn "Windows Update - additional resources" (page updated 2026-02-12), "Repair a Windows
Image" (updated 2021-12-15) and Get-WindowsUpdateLog. Removed as unconfirmed: the error-code table (0x800f081f, 0x80070002,
0x8024402c, 0x80070070), CBS.log, the `WIM:...install.wim` /Source syntax, stopping/renaming msiserver, the WSUS registry
policy key check, the 10-20 GB free space figure, manual `wusa` install, in-place repair install, and the gotchas about
catroot2 access denied and third-party fixers.
Method: documentation only; no commands were run.
