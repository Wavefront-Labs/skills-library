---
id: computing-software.systems-network-administration.patch-management.reset-windows-update-components
name: reset-windows-update-components
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reset-windows-update, failed-update-install, windowsupdate-log, dism, sfc, component-store]
level: practitioner
status: docs-checked
description: "Repair a Windows machine that keeps failing updates: read the error, repair the component store with DISM and SFC, reset SoftwareDistribution, or in-place upgrade."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/additional-resources-for-windows-update
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image
  - https://learn.microsoft.com/en-us/powershell/module/windowsupdate/get-windowsupdatelog
  - https://learn.microsoft.com/en-us/windows/deployment/update/windows-update-error-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resetting Windows Update components

Work from least to most invasive. Note the error code first (Settings → Update history,
`Get-WindowsUpdateLog` merges the Windows Update .etl files into a readable log, and the CBS log under `%windir%\Logs\CBS`).

## 1. Basics
- Free space on the system drive.
- Pending reboot? Restart first.
- Time/date and proxy/WSUS reachability (`Test-NetConnection wsus01 -Port 8530`).

## 2. Repair the component store
```cmd
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /RestoreHealth
DISM /Online /Cleanup-Image /RestoreHealth /Source:<REPAIR_SOURCE> /LimitAccess
sfc /scannow
```
Without `/Source`, DISM uses the default Features on Demand repair source (set by Group Policy). Use `/Source` with a matching-build repair source when the machine can't reach Windows Update; `/LimitAccess` stops DISM using Windows Update as a backup source. Run DISM before `sfc /scannow`.

## 3. Reset Windows Update cache
```powershell
Stop-Service wuauserv, bits, cryptsvc -Force
Rename-Item "$env:windir\SoftwareDistribution" "SoftwareDistribution.old" -EA 0
Rename-Item "$env:windir\System32\catroot2" "catroot2.old" -EA 0
Start-Service cryptsvc, bits, wuauserv
```
Microsoft's documented manual reset stops the BITS, Windows Update and Cryptographic services and renames `SoftwareDistribution\DataStore`, `SoftwareDistribution\Download` and `catroot2` to .bak; its simplest form is stop wuauserv, delete `SoftwareDistribution`, start wuauserv. The documented `sc.exe` step that resets BITS and Windows Update service security descriptors overwrites the existing ACLs: skip it unless the other steps failed.
Then trigger a scan from Settings or your management tool (ConfigMgr Software Updates Scan Cycle).

## 4. Install manually
Download the update package from the Microsoft Update Catalog and install it with
`dism /online /add-package /packagepath:<file>.cab` (`/Add-Package` is a documented online package-servicing option) or by running the .msu. The DISM error is often clearer.

## Common codes
| Code | Typical cause |
|---|---|
| 0x8024402C | WU_E_PT_WINHTTP_NAME_NOT_RESOLVED: proxy or target server name cannot be resolved |
| 0x80244022 | WU_E_PT_HTTP_STATUS_SERVICE_UNAVAIL: HTTP 503, service temporarily overloaded |
| 0x8024401C | WU_E_PT_HTTP_STATUS_REQUEST_TIMEOUT: HTTP 408, server timed out waiting for the request |
| Other codes (for example 0x800f08xx) | look up in the Windows Update error reference and CBS log before acting |

## Last resort
In-place upgrade (repair install) from same-version media keeping apps and data, or
rebuild for servers managed as cattle.

## Verify
Scan finds and installs the current LCU; build/UBR matches target; CBS.log has no new
corruption entries.

## Checked

Checked 2026-10-27 against Microsoft Learn: Windows Update additional resources (reset steps), Repair a Windows image (DISM), Get-WindowsUpdateLog, sfc, DISM package-servicing options and the Windows Update error reference.
- DISM `/ScanHealth`, `/CheckHealth`, `/RestoreHealth`, `/Source`, `/LimitAccess` behaviour and `sfc /scannow`: confirmed.
- Manual reset order (stop BITS, wuauserv, cryptsvc; rename DataStore, Download and catroot2; optional sc.exe ACL reset with its overwrite warning): confirmed.
- WU_E_PT error names for 0x8024402C, 0x80244022 and 0x8024401C: confirmed.
- Removed unconfirmed: 0x800f081f, 0x800f0906, 0x80073712, 0x800f0922, 0x80070002/3 meanings, the disk space figure, wusa switches, `UsoClient StartScan`, the `/Source:WIM:` syntax and the msiserver step.
Method: documentation only; no commands were run.
