---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.performance-monitor-counters-and-data-collector-sets
name: performance-monitor-counters-and-data-collector-sets
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, perfmon, performance-counters, logman, data-collector-set, relog, performance]
level: practitioner
status: draft
description: "Use Performance Monitor properly: the counters that matter with thresholds, logman data collector sets for long captures, relog to CSV, and the built-in system diagnostics report."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logman"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/relog"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-performance-problems-in-windows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# performance-monitor-counters-and-data-collector-sets

## Counters that answer most questions
| Counter | Worry when |
|---|---|
| `\Processor(_Total)\% Processor Time` | Sustained over 85% |
| `\Process(*)\% Processor Time` | Shows which process (divide by core count) |
| `\Memory\Available MBytes` | Under 10% of RAM |
| `\Memory\Pages/sec` with low available memory | Sustained high means paging |
| `\Process(*)\Private Bytes` | Steady growth over hours = leak |
| `\PhysicalDisk(*)\Avg. Disk sec/Read` and `/Write` | Over 0.020 (20 ms) on SSD-backed systems |
| `\PhysicalDisk(*)\Current Disk Queue Length` | Persistently high with high latency |
| `\Network Interface(*)\Bytes Total/sec` | Near link speed |

## Capture over time (the user's slowness is never on when you look)
```cmd
logman create counter SlowPC -c "\Processor(_Total)\% Processor Time" "\Process(*)\% Processor Time" "\Memory\Available MBytes" "\Process(*)\Private Bytes" "\PhysicalDisk(*)\Avg. Disk sec/Read" "\PhysicalDisk(*)\Avg. Disk sec/Write" -si 00:00:15 -f bincirc -max 512 -o "%ProgramData%\Perf\SlowPC"
logman start SlowPC
logman stop SlowPC
relog "%ProgramData%\Perf\SlowPC_000001.blg" -f csv -o "%TEMP%\SlowPC.csv"
```
- `bincirc` with `-max` caps disk use; 15-second samples for a day are small.
- Open the `.blg` in Performance Monitor (View log data) and ask the user for the time it
  felt slow.

## Built-in reports
- `perfmon /report` runs a 60-second System Diagnostics report with warnings.
- Resource Monitor (`resmon`) for live per-process disk and network.

## Gotchas
- `Process(*)` counters for short-lived processes miss them; use WPR for those.
- Counter names are localised on non-English Windows; use `typeperf -q` to list names.
- Leaving a collector running forever fills disks; set a stop condition or schedule.

## Verify
The log covers the slow period, the counters identify the bottleneck resource and
process, and the collector is stopped and removed (`logman delete SlowPC`).
