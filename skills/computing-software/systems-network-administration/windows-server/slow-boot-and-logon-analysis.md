---
id: computing-software.systems-network-administration.windows-server.slow-boot-and-logon-analysis
name: slow-boot-and-logon-analysis
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, winre, slow-logon, slow-boot, group-policy-processing, wpr-boottrace, diagnostics-performance]
level: advanced
status: draft
description: "Diagnose slow server boot and logon: Diagnostics-Performance events, Group Policy timings, verbose status messages, WPR boot traces and common culprits."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slow boot and logon analysis

## Quick evidence
- `Microsoft-Windows-Diagnostics-Performance/Operational`: event 100 (boot duration with
  MainPathBootTime, BootPostBootTime), 101-110 (degrading apps/drivers/services), 200
  (shutdown).
```powershell
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Diagnostics-Performance/Operational';Id=100} -MaxEvents 5 |
  % { $x=[xml]$_.ToXml(); [pscustomobject]@{Time=$_.TimeCreated; BootMs=($x.Event.EventData.Data | ? Name -eq BootTime).'#text'} }
```
- Group Policy: `Microsoft-Windows-GroupPolicy/Operational` events 4001/8001 (start/end
  computer/user processing), 5016 per CSE with duration, 5326 DC discovery time.
  `gpresult /h` shows component timing.
- Enable "Display highly detailed status messages" (GPO System) to see where logon sits.

## Usual culprits
| Symptom | Cause |
|---|---|
| "Please wait for the Group Policy Client" minutes | DC unreachable/slow site link, WMI filters, drive maps/printers in GPP, scripts with sync waits |
| "Preparing Windows" at logon | user profile load: big roaming profile, folder redirection offline |
| Long "Applying computer settings" | software installation GPO, slow startup scripts |
| Slow boot before logon screen | services with long timeouts (waiting for network), failing iSCSI/mapped dependencies, driver retries |
| Logon fast but desktop slow | Explorer shell extensions, Run keys, AV scanning profile |

## Deep dive: WPR boot trace
```
wpr -boottrace -addboot GeneralProfile -filemode -recordtempto <vol>:\Temp
# reboot, log on, wait for desktop
wpr -boottrace -stopboot <vol>:\Traces\boot.etl
```
Open in WPA with the Full Boot regions of interest: shows boot phases (PreSMSS, SMSS,
Winlogon init, Explorer init) and what each waited on.

## Fixes
- Remove sync script waits (`Run logon scripts synchronously` off), use GPP item-level
  targeting sparingly, fix WMI filters, ensure the client's site maps to a nearby DC.
- `Always wait for the network at computer startup and logon` only if needed.

## Verify
- [ ] Event 100 boot time and GP 8001 durations back to baseline.
