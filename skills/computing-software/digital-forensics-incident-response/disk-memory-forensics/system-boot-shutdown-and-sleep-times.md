---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.system-boot-shutdown-and-sleep-times
name: system-boot-shutdown-and-sleep-times
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [system-power-events, user-activity-artefacts, windows-event-logs, timezone-analysis, dfir]
level: practitioner
status: draft
description: "Establish when a Windows system was on, off, asleep or hibernated: kernel boot/shutdown events, power transitions, last shutdown time and uptime records."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System boot, shutdown and sleep times

**Goal:** many cases hinge on "was the computer on (and in use) at time X?". Reconstruct power
state intervals before interpreting user activity.

## Event log sources (System log unless noted)
| Event | Provider | Meaning |
|---|---|---|
| 12 | Kernel-General | OS started (boot time in data) |
| 13 | Kernel-General | OS shutting down |
| 6005 / 6006 | EventLog | Event log service started / stopped (boot / clean shutdown) |
| 6008 | EventLog | Previous shutdown was unexpected |
| 41 | Kernel-Power | Rebooted without clean shutdown (crash, power loss) |
| 1074 | User32 | Shutdown/restart initiated by a process/user, with reason |
| 42 | Kernel-Power | Entering sleep (reason) |
| 107 / 1 | Kernel-Power / Power-Troubleshooter | Resume from sleep (Power-Troubleshooter 1 gives sleep and wake times) |
| 506 / 507 | Kernel-Power | Modern Standby entering/exiting connected standby |
| 4800 / 4801 (Security) | | Workstation locked / unlocked (if auditing enabled) |

## Registry and other
- `SYSTEM\CurrentControlSet\Control\Windows\ShutdownTime` (FILETIME of last clean shutdown).
- SRUM records per-hour activity, giving on/off evidence even when event logs rolled.
- `%SystemRoot%\System32\LogFiles\` and `sleepstudy` reports (`powercfg /sleepstudy`) on Modern Standby devices.
- Logon/logoff 4624/4634 and lock/unlock for user presence.

## Build the table
Boot -> (sleep/resume pairs) -> shutdown, per day; mark gaps (no events = off or logs missing).

## Gotchas
- Fast Startup: "shutdown" is a hibernate of the kernel session; Kernel-General 12/13 and 6005/6006 still appear but uptime counters continue.
- Modern Standby devices are "on" while screen off; network activity continues.
- Event log retention may not cover the period; SRUM and other artefacts fill gaps.

## Verify
The power-state timeline is consistent across event logs, ShutdownTime and SRUM for the period of interest.
