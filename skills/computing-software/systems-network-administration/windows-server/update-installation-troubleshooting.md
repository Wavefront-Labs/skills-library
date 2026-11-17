---
id: computing-software.systems-network-administration.windows-server.update-installation-troubleshooting
name: update-installation-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-updates, servicing, update-failures, cbs-log, windowsupdate-log, get-windowsupdatelog, softwaredistribution, rollback-loop, pending-reboot, 0x800f0922, 0x80070002]
level: practitioner
status: docs-checked
description: "Diagnose failed or looping Windows Server updates: pending reboots, Get-WindowsUpdateLog, CBS.log, common codes and the rollback loop."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/common-windows-update-errors
  - https://learn.microsoft.com/en-us/powershell/module/windowsupdate/get-windowsupdatelog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot update installation failures

## 1. Is a reboot pending?
Many failures are just a pending reboot blocking the next install:
```powershell
Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction SilentlyContinue
```

## 2. Read the right log
- **Scan/download problems**: `Get-WindowsUpdateLog` merges the Windows Update ETL traces into one readable log
  (see its reference page for the default output path).
- **Install problems**: `%windir%\Logs\CBS\CBS.log`; Microsoft's error table says to search it for `error` and match the
  timestamp of the failure.

## 3. Common codes (per Microsoft's common-errors page)
| Code | Documented cause | Documented action |
|---|---|---|
| 0x800f081f / 0x800f0831 | component store corruption (source missing / store corrupted) | `Dism.exe /Online /Cleanup-Image /Restorehealth`, `Sfc.exe /Scannow`, restart |
| 0x800f0922 | on Server 2016, licence/product-key tokens fail to update and the update rolls back | add write permission for "User" and "Network Service" on `%windir%\System32\spp\` |
| 0x80070003 | servicing stack cannot reach a path (invalid path to an executable) | find the error in the last CBS.log by timestamp |
| 0x80070bc9 | TrustedInstaller start type forced to Manual by GPO, so a post-restart transaction cannot complete | set the policy back to Automatic and restart; else boot WinRE and run `dism /Image:<WINDOWS_DRIVE>:\ /Cleanup-Image /RevertPendingActions` |
| 0x80244022 | HTTP 503 from the update source | network/proxy troubleshooting to the update source |
| 0x8024401B | proxy authentication required (407) | fix WinHTTP/WinInet proxy settings |
| 0x80072F8F | TLS 1.2 not configured on the client | install the update in KB3140245 |

## 4. Rollback loop
If an update fails during the offline phase on every boot, start WinRE and revert pending actions with
`dism /Image:<WINDOWS_DRIVE>:\ /Cleanup-Image /RevertPendingActions`, as in the 0x80070bc9 row above.

## Verify
- [ ] The update appears in the installed updates list.
- [ ] No pending-reboot flags remain after the restart.

## Checked
2026-10-28. Confirmed on Learn "Common Windows Update errors" and Get-WindowsUpdateLog pages: every code row above,
RevertPendingActions command, CBS.log search advice. Removed: FATAL/0x8024 log hints, 0x80070002/0x8024401c rows
(not on the page; 0x80244022 and 0x80070003 causes corrected), the SoftwareDistribution/catroot2 reset recipe and
Get-HotFix/event 2 verify step (not confirmed in the fetched pages).
Method: documentation only; no commands were run.
