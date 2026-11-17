---
id: computing-software.systems-network-administration.windows-server.secure-time-seeding
name: secure-time-seeding
category: computing-software
field: systems-network-administration
product: windows-server
tags: [w32time, secure-time-seeding, clock-skew, windows-time-service, domain-controller]
level: advanced
status: docs-checked
description: "Understand Secure Time Seeding (UtilizeSslTimeData): how SSL timestamps can jump server clocks, why to disable it on DCs and servers, and detecting jumps."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-server-2016-improvements
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/configure-authoritative-time-server
  - https://learn.microsoft.com/en-us/archive/blogs/w32time/secure-time-seeding-improving-time-keeping-in-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure Time Seeding

From Windows 10 build 1511 and Windows Server 2016, W32Time can estimate the current time from outgoing SSL
connections ("Secure Time Seeding", STS) and use it to monitor the local clock and correct gross errors. The
registry value is `UtilizeSslTimeData`; its out-of-box default is 1 on every version that has the feature except
Windows Server 2025, where the default is 0. Microsoft's guidance is that deployments with reliable time sources
and offset monitoring may choose not to use the feature.

## Symptoms
- Sudden large time change with no admin action (clock set directly; W32Time logs an audit event when a direct
  correction exceeds `TimeJumpAuditOffset`).
- On a DC: Kerberos failures domain-wide and replication refusing partners over time differences.

## Disable on servers (where reliable sources and offset monitoring exist)
```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config /v UtilizeSslTimeData /t REG_DWORD /d 0 /f
w32tm /config /update
```
`/config /update` stops time monitoring and enforcement from SSL data immediately; data collection stops after a
reboot. To cover a domain, set `UtilizeSslTimeData` to 0 in the W32Time Group Policy setting (ADMX_W32Time) and
exclude portable laptops and tablets, which may need STS to bootstrap their time after battery drain.

## Belt and braces: phase correction limits
Limit how far the service will move the clock without admin action, especially on the PDC. Documented defaults:
0xFFFFFFFF (always correct) on domain members, 172800 s (48 h) on domain controllers, 54000 s (15 h) on stand-alone
servers. Microsoft's authoritative-time-server article names 3600 or 1800 s as reasonable values for a PDC; pick one
to suit the poll interval, network and upstream source:
```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config /v MaxPosPhaseCorrection /t REG_DWORD /d 3600 /f
reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config /v MaxNegPhaseCorrection /t REG_DWORD /d 3600 /f
```
Values in seconds; if a larger change is required the service logs an event instead of applying it.

## Detect jumps
```powershell
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Time-Service'} -MaxEvents 30 |
  Select-Object TimeCreated,Id,Message
```
Review time-service events around any unexplained jump; set `TimeJumpAuditOffset` (seconds) to the smallest direct
correction you want audited.

## Verify
- [ ] UtilizeSslTimeData = 0 on all DCs; `w32tm /query /configuration` shows MaxPos/MaxNegPhaseCorrection limits.

## Checked

2026-10-27. Documentation release: Windows Server time service documentation (windowsserverdocs, current 2025/2026 pages). Confirmed from the Windows Time Service Tools and Settings registry reference: UtilizeSslTimeData default 1 except Windows Server 2025 (0); MaxPos/MaxNegPhaseCorrection defaults and the log-an-event behaviour; TimeJumpAuditOffset. Confirmed from the Windows Server 2016 time improvements page: the disable procedure, /config /update behaviour, reboot behaviour and the laptop exemption. Confirmed from the authoritative time server article: 3600 or 1800 as reasonable correction limits. Removed unconfirmed event IDs, the early-tombstoning claim and the GPO Preferences advice.

Method: documentation only; no commands were run.
