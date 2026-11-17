---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.intermittent-fault-strategies
name: intermittent-fault-strategies
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, intermittent-faults, fault-diary, logging, reproduction, monitoring, procmon]
level: practitioner
status: draft
description: "Pin down faults that come and go: fault diaries, always-on logging and ring-buffer captures, recording the next occurrence, controlled variable changes and environmental factors."
sources:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/procmon"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logman"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# intermittent-fault-strategies

Never close an intermittent fault as "cannot reproduce" without a plan to catch the next
one.

## 1. Fault diary
Ask the user to note the exact time, what they were doing, where (desk, home, meeting
room, docked), and what they saw, each time. Three entries usually reveal a pattern:
time of day, location, after sleep, on battery, during calls.

## 2. Leave capture running
- Perfmon data collector in circular mode (see
  performance-monitor-counters-and-data-collector-sets).
- Process Monitor with "Drop Filtered Events" and a backing file, or boot logging for
  startup faults; stop it right after the next occurrence.
- Continuous ping to gateway and a server with timestamps for network drops:
  `ping -t 10.0.0.1 | ForEach-Object { "{0} {1}" -f (Get-Date -Format s), $_ } >> "$env:TEMP\ping.log"`
- Reliability Monitor and event logs already record history; check them first.

## 3. Record the next occurrence
User presses `Win`+`Shift`+`S` or uses Snipping Tool screen recording to capture error
text, then notes the time in the ticket. The timestamp ties symptom to logs.

## 4. Change one variable at a time
Swap dock, cable, charger, Wi-Fi vs Ethernet, user profile, or device, one per cycle,
and wait long enough to see whether it recurs (at least the normal interval between
failures times two).

## 5. Think environment
Heat (afternoon sun, closed cabinets), power (shared circuits, UPS), Wi-Fi roaming between
access points, sleep and wake, VPN reconnects, scheduled tasks and backups at fixed
times, physical movement (loose cable, hinge).

## Gotchas
- Users stop reporting once they find a workaround; agree how long you will monitor.
- Too many simultaneous changes "fix" it without telling you what the cause was.

## Verify
The fault has been captured with logs at the moment of failure, the cause is fixed, and no
recurrence over at least twice the previous longest gap.
