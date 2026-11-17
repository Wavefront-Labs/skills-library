---
id: computing-software.systems-network-administration.windows-server.w32time-debug-logging
name: w32time-debug-logging
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, time-service, w32time-debug-log, time-events, w32tm, troubleshooting]
level: advanced
status: docs-checked
description: "Turn on W32Time debug logging with w32tm /debug and read Time-Service events 36 and 142 to find why a server's clock is wrong or not syncing."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/turn-on-debug-logging-in-windows-time-service
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/w32time-event-142-time-service-stopped-advertising
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# W32Time debug logging and time events

## Events (System log, source Time-Service)
| ID | Meaning |
|---|---|
| 36 | a DC that cannot reach a time source logs it after repeated attempts |
| 142 | time service stopped advertising as a time source; the message text gives the cause (not a DC, no providers running, or not a good time source) |

`EventLogFlags` (Config) selects what is logged: 0x1 time jump, 0x2 source change (default 2). Look up other IDs
in the Time-Service event documentation before relying on them.
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-Time-Service'} -MaxEvents 30 | ft TimeCreated,Id,Message -Wrap
```

## Debug log
```cmd
w32tm /debug /enable /file:<LOGS>\w32time.log /size:10000000 /entries:0-300
REM reproduce: w32tm /resync /rediscover
w32tm /debug /disable
```
`/file` takes an absolute file name, `/size` is the maximum size in bytes for circular logging, `/entries` takes
flags 0 to 300 (a range such as 0-100,103,106 is valid; 0-300 logs everything). Microsoft recommends debug logging
only after other troubleshooting, and says the detailed output may need Microsoft Support to interpret. Turn it off
afterwards.

Registry alternative (Config key, then restart W32Time): `FileLogSize` DWORD (bytes), `FileLogName` string (path),
`FileLogEntries` string, for example `0-116`.

## Quick checks
```cmd
w32tm /query /status /verbose      REM source, stratum, last sync, poll interval
w32tm /query /peers                REM state of each peer
w32tm /monitor /domain:ad.example.com   REM offsets of all DCs vs PDC
w32tm /stripchart /computer:pool.ntp.org /dataonly /samples:5
```
"Local CMOS Clock" or "Free-running System Clock" as source = not syncing at all.

## Typical causes
- UDP 123 blocked (the NTP client needs UDP 123 as its source port) to the PDC root's external sources.
- Hyper-V time sync integration fighting NT5DS on a DC.
- VM restored or host clock wrong; a required change bigger than MaxPos/MaxNegPhaseCorrection is logged, not applied.

## Verify
- [ ] No event 142/36 after the fix; `w32tm /monitor` shows all DCs close to the PDC.

## Checked

2026-10-27. Documentation release: windowsserverdocs time pages (current) and the Support Articles page last dated 2026-02-12. Confirmed: w32tm /debug syntax and entries range 0-300; registry-based debug logging values; event 142 text and causes (Microsoft-Windows-Time-Service); event 36 on DC after repeated failures; /resync options (/rediscover; there is no /force); /query, /monitor and /stripchart switches; EventLogFlags values; phase correction behaviour. Removed event IDs 24, 29, 35, 37, 47, 50, 129 and 134 and the log keyword claims because no fetched page covers them.

Method: documentation only; no commands were run.
