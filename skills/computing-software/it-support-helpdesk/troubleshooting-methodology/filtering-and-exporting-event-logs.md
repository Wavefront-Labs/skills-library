---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.filtering-and-exporting-event-logs
name: filtering-and-exporting-event-logs
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, evidence-gathering, log-analysis, event-log-filtering, event-viewer, get-winevent, filterhashtable, custom-views, wevtutil, evtx]
level: practitioner
status: draft
description: "Get signal out of Windows event logs: custom views and XML filters, Get-WinEvent with FilterHashtable, time-window correlation, useful event IDs, and exporting EVTX for escalation."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil"
  - "https://learn.microsoft.com/en-us/windows/win32/wes/consuming-events"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# filtering-and-exporting-event-logs

Goal: find the handful of relevant events among thousands, around the time
the problem happened, and hand them to L2/vendors in a usable form.

## Event Viewer
- **Filter Current Log**: level (Critical/Error/Warning), event IDs (e.g.
  `41,1001,6008`), source, time window.
- **Create Custom View** across several logs (System + Application +
  specific Operational logs) — save as "Crash triage", reuse.
- Applications and Services Logs → Microsoft → Windows → component
  `Operational` logs hold the useful detail (WLAN-AutoConfig,
  DeviceManagement-Enterprise-Diagnostics-Provider, PrintService, GroupPolicy,
  TerminalServices).
- XML tab of a filter allows XPath for precise queries.

## PowerShell
```powershell
# errors and criticals in System in the hour around the incident
$t = Get-Date '2026-10-16 09:40'
Get-WinEvent -FilterHashtable @{LogName='System','Application'; Level=1,2; StartTime=$t.AddMinutes(-30); EndTime=$t.AddMinutes(30)} |
  Select TimeCreated, LogName, ProviderName, Id, LevelDisplayName, Message | Format-Table -Wrap
# specific IDs on a remote machine
Get-WinEvent -ComputerName PC01 -FilterHashtable @{LogName='System'; Id=41,6008,1074}
# list logs that have recent records
Get-WinEvent -ListLog * | Where RecordCount -gt 0 | Sort LastWriteTime -Desc | Select -First 20 LogName, LastWriteTime
```
FilterHashtable filters at source — much faster than `Where-Object` after.

## Handy IDs
| ID | Log/Source | Meaning |
|---|---|---|
| 41 | Kernel-Power | unexpected restart |
| 6008 | EventLog | previous shutdown unexpected |
| 1074 | User32 | who/what initiated a restart |
| 1001 | BugCheck/WER | BSOD / app crash report |
| 1000 / 1002 | Application Error / Hang | app crash / hang |
| 7031 / 7034 | Service Control Manager | service crashed |
| 4625 / 4740 | Security | failed logon / lockout |
| 1129 / 1053 | GroupPolicy | GP processing failures |

## Export for escalation
- Event Viewer: Save Filtered Log File As… (.evtx, include display
  information).
- `wevtutil epl System %TEMP%\System.evtx "/q:*[System[TimeCreated[timediff(@SystemTime) <= 86400000]]]"`
- Zip and attach to the ticket with the incident time noted.

## Gotchas
- Logs roll over (default size small) — export soon after the event or
  increase log size via policy.
- Warnings are often noise; correlate by time with the user's report.

## Verify
The ticket references specific event IDs/timestamps tied to the problem,
with exported EVTX attached when escalated.
