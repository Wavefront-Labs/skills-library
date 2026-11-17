---
id: computing-software.systems-network-administration.windows-server.disable-dedup-and-unoptimize-volume
name: disable-dedup-and-unoptimize-volume
category: computing-software
field: systems-network-administration
product: windows-server
tags: [data-deduplication, unoptimization, start-dedupjob, disable-dedupvolume, storage-capacity]
level: advanced
status: docs-checked
description: "Remove Data Deduplication from a volume: capacity planning for rehydration, running the Unoptimization job, garbage collection and disabling cleanly."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/run
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/interop
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/disable-dedupvolume
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/start-dedupjob
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling dedup and unoptimizing a volume

Simply disabling dedup (`Disable-DedupVolume`) leaves the volume in a deduplicated state: existing data stays accessible
through the dedup filter, but nothing is rehydrated and new data is not optimised.

## 1. Capacity check
Rehydration needs space for the **logical** size of all optimised files:
```powershell
Get-DedupVolume D: | Format-List *      # compare the logical (unoptimised) size with the volume capacity
```
The Unoptimization job fails if the volume does not have enough space for the unoptimised data. If it will not fit,
extend the volume or move data off first. Microsoft does not recommend Robocopy against dedup volumes because some
commands can corrupt the chunk store.

## 2. Unoptimize
```powershell
Start-DedupJob -Volume D: -Type Unoptimization -Memory 50
Get-DedupJob                         # Progress
```
The job undoes the optimisation and disables Data Deduplication for the volume. It is I/O heavy on large volumes, so
schedule it out of hours.

## 3. Clean the chunk store
```powershell
Start-DedupJob -Volume D: -Type GarbageCollection -Full
```
This frees chunks that nothing references any more.

## 4. Disable and remove
```powershell
Disable-DedupVolume D:
Get-DedupStatus                       # D: no longer listed
Uninstall-WindowsFeature FS-Data-Deduplication   # only if no volume uses dedup
```
Do not uninstall the feature while optimised files remain; run the Unoptimization job first.

## Verify
- [ ] `Get-DedupStatus` no longer lists D: after `Disable-DedupVolume`; `Get-DedupVolume` shows it disabled or absent.
- [ ] Volume free space matches expectations; applications read files normally.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed that Disable-DedupVolume leaves existing data deduplicated and accessible, the Unoptimization job (manual only, disables dedup for the volume, fails without enough space), Start-DedupJob -Type GarbageCollection -Full, and the Robocopy warning. Removed the unconfirmed claims on days-long runtimes, pause and restart, directory shrinkage, unreadable files after uninstall, the SavedSpace field and the reparse-point check.

Method: documentation only; no commands were run.
