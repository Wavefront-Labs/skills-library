---
id: computing-software.it-support-helpdesk.remote-support-tools.rmm-monitors-and-alert-thresholds
name: rmm-monitors-and-alert-thresholds
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rmm-monitoring, rmm, alerting, alert-fatigue, thresholds, auto-ticketing, psa-integration]
level: practitioner
status: draft
description: "Design RMM monitors that catch real faults without flooding the queue: sustained thresholds, service and event monitors, auto-resolve, maintenance windows and tuning."
sources:
  - "https://sre.google/sre-book/monitoring-distributed-systems/"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practice-manager"
  - "https://learn.microsoft.com/en-us/windows/win32/eventlog/event-logging"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rmm-monitors-and-alert-thresholds

## Principles
- Alert only on conditions someone must act on; everything else is a report.
- Every alert maps to a runbook or KB article and a priority.
- Prefer sustained conditions over spikes: "CPU over 90% for 15 minutes" not "CPU over 90%".

## Starter set for workstations and servers
| Monitor | Threshold that works | Notes |
|---|---|---|
| Disk free | Below 10% and below 10 GB (both) | Percent alone fires on big data drives |
| Agent offline | Servers 10 min; laptops do not alert | Laptops go offline every evening |
| Service stopped | Critical services set to Automatic | Exclude Automatic (Delayed/Trigger) services that stop normally |
| Event log | Specific IDs: disk 7/51/153, NTFS 55, unexpected shutdown 41/6008 | Never "any Error" |
| Backup | Last success older than 26 hours | Covers a daily job that ran late |
| AV/EDR | Disabled, outdated signatures over 3 days, threat detected | Threat detected = P2 ticket |
| Patch | Pending reboot over 7 days | Drives user comms rather than a tech |

## Ticket flow
- Auto-create tickets for actionable alerts with device, monitor, value and runbook link.
- Auto-resolve when the condition clears, but keep the ticket for repeat-offender stats.
- De-duplicate: one open ticket per device per monitor.
- Maintenance windows suppress alerts during patching and known reboots.

## Tuning loop
Monthly, export alerts by monitor: anything closed as "no action" more than half the
time gets a higher threshold, a longer duration, or deletion. Track alerts per device
per month as the noise metric.

## Gotchas
- Self-healing scripts attached to monitors hide recurring faults; log every run and
  review counts.
- Thresholds copied from vendor templates assume servers; workstation policies need their
  own set.

## Verify
A simulated fault (stop a monitored service, fill a test disk) creates exactly one ticket
with the right priority, and clearing it auto-resolves.
