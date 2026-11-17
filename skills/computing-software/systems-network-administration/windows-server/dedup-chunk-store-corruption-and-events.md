---
id: computing-software.systems-network-administration.windows-server.dedup-chunk-store-corruption-and-events
name: dedup-chunk-store-corruption-and-events
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dedup, dedup-chunk-store, data-deduplication, scrubbing, event-log]
level: advanced
status: docs-checked
description: "Diagnose Data Deduplication chunk store corruption: read Deduplication events, run scrubbing jobs, find affected files and restore them from backup."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/understand
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/run
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/start-dedupjob
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/set-dedupvolume
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedup chunk store corruption and events

Optimized files are reparse points pointing at chunks in `System Volume Information\Dedup\ChunkStore`. A damaged
chunk can affect many files, so corruption matters more on dedup volumes.

## Events
Applications and Services Logs > Windows > Deduplication > **Operational** (the documented place for job success and failure detail):
- Scrubbing repairs corrupted chunks from a redundant copy when one exists: a hotspot copy of a popular chunk, or a Storage Spaces mirror or parity reconstruction.
```powershell
Get-WinEvent -LogName 'Microsoft-Windows-Deduplication/Operational' -MaxEvents 50 | ft TimeCreated,Id,Message -Wrap
Get-DedupStatus | fl Volume,LastScrubbingTime,LastScrubbingResult,LastScrubbingResultMessage    # 0 = success
```

## Run a scrub now
```powershell
Start-DedupJob -Volume E: -Type Scrubbing                # validates critical metadata and previously seen problems
Start-DedupJob -Volume E: -Type Scrubbing -Full          # validates all data on the volume, slow
Get-DedupJob
```
Run a full scrub after storage incidents (controller faults, power loss, disk replacement).

## When files are unrepairable
1. Take the affected file list from the Operational log entries for the scrubbing job.
2. Restore those files from backup (dedup-aware restore; see backup-restore-deduplicated-volumes).
3. If corruption is widespread, check the storage layer first (disk errors in System log, `Get-PhysicalDisk`
   health, `chkdsk /scan`).

## Make repairs possible
- Dedup keeps backup copies of popular chunks in the hotspot area once they are referenced more than 100 times (`ChunkRedundancyThreshold`, default 100, minimum 20).
- On a Storage Spaces mirror or parity volume, dedup can use the volume's redundancy to reconstruct corrupted data.

## Verify
- [ ] Latest scrub result OK with zero unrepairable corruptions; affected files restored and readable.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed the scrubbing job purpose and repair sources (hotspot copies, mirror or parity), the 100-reference hotspot and ChunkRedundancyThreshold default 100 and minimum 20, Start-DedupJob -Type Scrubbing with and without -Full, LastScrubbingResult 0 = success, and the Deduplication Operational log. Removed the unconfirmed Scrubbing channel name and the OptimizedFilesCount field.

Method: documentation only; no commands were run.
