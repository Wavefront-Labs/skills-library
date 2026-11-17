---
id: computing-software.systems-network-administration.windows-server.dedup-optimization-gc-and-scrubbing-jobs
name: dedup-optimization-gc-and-scrubbing-jobs
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, data-deduplication, dedup, dedup-jobs, start-dedupjob, garbage-collection, scrubbing, dedup-schedule, set-dedupschedule]
level: practitioner
status: docs-checked
description: "Run and schedule dedup Optimization, GarbageCollection and Scrubbing jobs: windows, throughput, memory limits and reading job results and corruption events."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/understand
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/advanced-settings
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/run
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/start-dedupjob
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/new-dedupschedule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedup Optimization, Garbage Collection and Scrubbing jobs

## Job types
| Job | Does | Default schedule |
|---|---|---|
| Optimization | chunks and compresses files into the chunk store | once every hour |
| GarbageCollection | frees chunks no longer referenced (after deletes or changes) | Saturday 2:35 AM |
| Scrubbing | verifies chunk store integrity, repairs from redundant copies | Saturday 3:35 AM |
| Unoptimization | rehydrates all files | manual only |

Space from deleted or modified files is only reclaimed when GarbageCollection runs. A regular run frees space after a threshold of deleted data; `-Full` frees everything and the cmdlet docs suggest running it about monthly.

## Run on demand
```powershell
Start-DedupJob -Volume 'E:' -Type GarbageCollection -Full    # -Full frees all unreferenced data
Start-DedupJob -Volume 'E:' -Type Scrubbing -Full             # validates all data on the volume
Get-DedupJob | Select Type,State,Progress,Volume
Stop-DedupJob -Volume 'E:'
```

## Custom schedules (busy servers)
```powershell
Get-DedupSchedule
Set-DedupSchedule -Name BackgroundOptimization -Enabled $false
New-DedupSchedule -Name NightlyOpt -Type Optimization -Days @(1,2,3,4,5) `
  -Start (Get-Date '2016-08-08 22:00:00') -DurationHours 8 -Memory 50 -Cores 50 -Priority High
```
- `-Memory` and `-Cores` are percentages (0-100); `-Days` takes integers (0 = Sunday, 6 = Saturday).
- Schedules run through Task Scheduler under Microsoft\Windows\Deduplication; `Remove-DedupSchedule` deletes one.
- If jobs cannot keep up with churn, the optimisation rate trends down: lengthen the window or raise `-Memory`.

## Results and corruption
- Events in `Applications and Services Logs\Windows\Deduplication\Operational`.
- `Get-DedupStatus | fl` shows LastOptimizationResult, LastGarbageCollectionResult,
  LastScrubbingResult (0 = success).
- If scrubbing cannot repair corrupted chunks, restore the affected files from backup.

## Verify
- [ ] All three Last*Result values are 0.
- [ ] `Get-DedupStatus E:` SavingsRate and OptimizedFilesSavingsRate trending as expected.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed the job table and default schedules (hourly optimization, Saturday 2:35 AM garbage collection, Saturday 3:35 AM scrubbing, on-demand-only unoptimization), -Full semantics for GarbageCollection and Scrubbing, schedule cmdlets and the -Days numbering, Memory and Cores as 0-100 percentages, the Last*Result 0 = success fields, and the Operational log path. Corrected the garbage collection and scrubbing start times (were 02:45 and 03:45). Removed the unconfirmed 25 percent default, throughput figure and per-core-group advice.

Method: documentation only; no commands were run.
