---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.disk-at-100-percent-usage
name: disk-at-100-percent-usage
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, storage-troubleshooting, disk-100-percent, disk-queue-length, resource-monitor, slow-disk, search-indexer, sysmain, storport-errors, hdd-to-ssd]
level: practitioner
status: draft
description: "Diagnose disk-at-100% slowness on Windows: Resource Monitor queue and response time, indexer/AV/update/sync causes, failing or SMR drives, and HDD upgrades."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server"
  - "https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning"
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/process-monitor"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# disk-at-100-percent-usage

Goal: identify what's hammering the disk, and whether the disk itself is the
problem.

## Measure, don't guess
Task Manager's "100 %" is **active time**, not throughput. Open Resource
Monitor (`resmon`) → Disk:
- **Processes with Disk Activity**: sort by Total (B/sec) — who's doing I/O.
- **Disk Activity**: the files being read/written (pagefile.sys, search
  database, OneDrive cache, AV definitions).
- **Storage**: **Disk Queue Length** and **Response time (ms)**.
Interpretation: response times > 20–50 ms sustained on an SSD or > 100 ms on
HDD = disk can't keep up. High active time with tiny throughput = slow or
failing drive.

## Usual causes
| Cause | Evidence | Fix |
|---|---|---|
| Spinning HDD in 2020s Windows | MediaType HDD in `Get-PhysicalDisk` | replace with SSD (the real fix) |
| Windows Update / servicing after patch Tuesday | TiWorker.exe, TrustedInstaller | let it finish, then reassess |
| Search indexing | SearchIndexer.exe, Windows.edb | let it finish; rebuild if looping |
| AV full scan / exclusions missing | MsMpEng.exe reading everything | schedule scans off-hours |
| OneDrive initial sync / reset | OneDrive.exe | wait; Files On-Demand |
| Paging (RAM too small) | heavy pagefile.sys I/O, high committed memory | more RAM, fewer apps |
| Failing drive | Event IDs 7/51/153, storport 129 resets, SMART | replace |
| SMR HDD under heavy writes | throughput collapses on sustained writes | SSD |

## Event log signs of hardware trouble
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='disk','storahci','stornvme','storport'; StartTime=(Get-Date).AddDays(-7)} |
  Select TimeCreated, Id, ProviderName, Message -First 30
```
Event 153 (IO retried), 129 (reset to device), 7 (bad block) → check SMART
and cabling/firmware.

## Gotchas
- Disabling SysMain/Search "to fix 100 % disk" hides the symptom and makes
  the PC slower elsewhere — only as a short diagnostic test.
- Storage drivers: outdated Intel RST/AMD SATA drivers cause high latency —
  update from the OEM.
- Process Monitor capture (filter on the top process) shows exact files when
  resmon isn't enough.

## Verify
After the fix, disk active time averages well under 50 % during normal use
and response time stays below 10–20 ms (SSD) in resmon.
