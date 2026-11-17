---
id: computing-software.systems-network-administration.windows-server.dedup-savings-evaluation-ddpeval
name: dedup-savings-evaluation-ddpeval
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, data-deduplication, dedup, ddpeval, get-dedupstatus, savings-estimate, capacity-planning]
level: intro
status: docs-checked
description: "Estimate dedup savings before enabling with DDPEval.exe, then measure real savings with Get-DedupStatus and Get-DedupVolume and explain gaps."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/install-enable
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/overview
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/run
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/update-dedupstatus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluate dedup savings: DDPEval and Get-DedupStatus

## Before enabling: DDPEval
`DDPEval.exe` is installed with the dedup feature in `%SystemRoot%\System32`. It evaluates directly connected volumes
(local drives or Cluster Shared Volumes) and mapped or unmapped network shares:
```powershell
DDPEval.exe <VOLUME>:\<FOLDER>
```
Output: evaluated folder, processed files and size, optimized size, space savings and percent (with and without
compression), files with duplication and files excluded by policy or error.

Typical savings per the Microsoft overview:
| Content | Savings |
|---|---|
| User documents | 30-50% |
| Deployment shares | 70-80% |
| Virtualization libraries (ISOs, virtual hard disks) | 80-95% |
| General file share | 50-60% |

## After enabling: measured savings
```powershell
Get-DedupStatus -Volume E: | Format-List *      # cached values: SavingsRate, OptimizedFilesSavingsRate, LastOptimizationTime
Update-DedupStatus -Volume E:                    # rescans the volume for fresh savings figures, volumes processed serially
```
- `OptimizedFilesSavingsRate` covers only in-policy optimized files; `SavingsRate` covers the whole volume.
- A downward-trending rate suggests Optimization jobs are not keeping up with churn: extend the job window.
- Low savings: files younger than MinimumFileAgeDays, excluded types, or files at or under the MinimumFileSize floor (32 KB).

## Report
Track `SavingsRate` over time. A falling rate can mean optimization is behind; also check `LastGarbageCollectionResult`.

## Verify
- [ ] Estimate recorded before enabling, actual after two weeks compared.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed DDPEval location and sample output fields, supported targets, the typical-savings table in the dedup overview, SavingsRate versus OptimizedFilesSavingsRate, Update-DedupStatus behaviour and the 32 KB MinimumFileSize floor. Removed the unconfirmed /V and /O switches, the backup-target and media rows, and the SavedSpace and InPolicyFilesCount fields.

Method: documentation only; no commands were run.
