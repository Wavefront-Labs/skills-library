---
id: computing-software.systems-network-administration.windows-server.dedup-exclusions-and-file-age-policy
name: dedup-exclusions-and-file-age-policy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [data-deduplication, dedup-exclusions, set-dedupvolume, dedup-jobs, minimumfileagedays]
level: practitioner
status: docs-checked
description: "Tune Data Deduplication policy: MinimumFileAgeDays, excluded folders and file types, chunk size behaviour and what not to dedup."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/advanced-settings
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/interop
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/set-dedupvolume
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/expand-dedupfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedup exclusions and file age policy

## Volume policy
```powershell
Get-DedupVolume D: | Format-List *
Set-DedupVolume D: -MinimumFileAgeDays 3 -ExcludeFolder '<DATA_VOLUME>\Shares\Scratch','<DATA_VOLUME>\Shares\SQLDumps' -ExcludeFileType 'pst','edb','ldf'
```
| Setting | Default | Notes |
|---|---|---|
| MinimumFileAgeDays | 3 for Default and HyperV usage types, 0 for Backup | days after file creation before a file is in policy |
| MinimumFileSize | must be greater than 32 KB | files below the threshold are not optimised |
| ExcludeFolder | none | full paths are accepted; mount points are ignored |
| ExcludeFileType | none | extensions without a leading period; setting it overrides existing values |
| NoCompress / NoCompressionFileType | compression on | turn off compression for all files or for listed types |
| OptimizeInUseFiles / OptimizePartialFiles | Default: no/no; HyperV: yes/yes; Backup: yes/no | partial files apply MinimumFileAge to file segments |

## What to exclude
- Files constantly rewritten in place, such as database files and open VM disks on general file shares.
- Folders with files that are deleted within days (scratch, temp exports).
- Already compressed data (multimedia and similar) compresses poorly; use `NoCompressionFileType` to save CPU.

## Changing policy later
New exclusions do not unoptimise files already deduplicated; previously optimised files under an excluded folder stay optimised until you unoptimise them. To rehydrate those
files: `Expand-DedupFile -Path <DATA_VOLUME>\Shares\SQLDumps\*` (Expand-DedupFile expands an optimized file back to its original location; check free space first).

## Gotchas
- `MinimumFileAgeDays 0` is the Backup usage type default; on general file shares it optimises hot files, which adds read latency.
- DFS Replication works with dedup: optimising or unoptimising a file does not trigger replication.

## Verify
- [ ] `Get-DedupStatus D:` shows SavingsRate and OptimizedFilesSavingsRate stable after the change.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed MinimumFileAgeDays defaults (3 for Default and HyperV, 0 for Backup), MinimumFileSize above 32 KB, ExcludeFolder and ExcludeFileType semantics, NoCompress and NoCompressionFileType, OptimizeInUseFiles/OptimizePartialFiles per usage type, that exclusions do not unoptimise existing files, Expand-DedupFile, and DFS Replication interoperability. Removed the unconfirmed field list, VDI-setting row and several generic exclusion examples.

Method: documentation only; no commands were run.
