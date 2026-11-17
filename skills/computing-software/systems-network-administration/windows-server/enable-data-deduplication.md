---
id: computing-software.systems-network-administration.windows-server.enable-data-deduplication
name: enable-data-deduplication
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, data-deduplication, dedup, enable-dedupvolume, usage-type, hyper-v-vdi, backup-target, fs-data-deduplication]
level: practitioner
status: docs-checked
description: "Install and enable Data Deduplication on a volume with the right usage type (Default, HyperV, Backup), exclusions and minimum file age."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/install-enable
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/understand
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/interop
  - https://learn.microsoft.com/en-us/powershell/module/deduplication/enable-dedupvolume
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable Data Deduplication with the right usage type

## Install
```powershell
Install-WindowsFeature FS-Data-Deduplication -IncludeManagementTools
```

## Pick the usage type
| UsageType | Workload | Behaviour |
|---|---|---|
| Default | general purpose file servers: team shares, work folders, folder redirection, software development shares | background optimisation, minimum file age 3 days |
| HyperV | VDI servers | background optimisation, age 3 days, optimises in-use and partial files |
| Backup | virtualised backup applications such as DPM | priority optimisation, age 0 days, optimises in-use files |

```powershell
Enable-DedupVolume -Volume 'E:' -UsageType Default
Set-DedupVolume -Volume 'E:' -MinimumFileAgeDays 3 -ExcludeFolder '<vol>:\Scratch' -ExcludeFileType 'mp4','zip'
```
- General purpose Hyper-V hosts, SQL servers and line-of-business servers may or may not benefit: evaluate them first
  (DDPEval, pilot). Random-read database patterns suffer most on HDDs.
- The cmdlet reference says dedup is unsupported on non-NTFS volumes (ReFS is supported from Windows Server 2019) and on volumes under 2 GB, and that
  with the HyperV usage type the deduplicating server cannot be the Hyper-V host itself.
- Multimedia and other already-compressed files compress poorly; use `NoCompressionFileType` to save CPU.
- Windows Server 2016 and later support volumes up to 64 TB; plan memory as at least 300 MB + 50 MB per TB of logical data (1 GB per TB is optimal).

## First run
Optimisation runs as a scheduled background job (hourly by default). Kick it off once instead of waiting:
```powershell
Start-DedupJob -Volume 'E:' -Type Optimization -Memory 50
Get-DedupJob
```

## Gotchas
- The chunk store lives in `System Volume Information`; deleting that folder corrupts the optimised files.
- Disabling dedup (`Disable-DedupVolume`) stops new optimisation but leaves existing data deduplicated and accessible;
  run `Start-DedupJob -Type Unoptimization` to rehydrate, which fails without enough free space for the unoptimised data.

## Verify
- [ ] `Get-DedupVolume` shows the volume with the intended UsageType.
- [ ] `Get-DedupStatus` shows SavingsRate rising and LastOptimizationResult 0 after the first job.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs Deduplication cmdlet pages. Confirmed Install-WindowsFeature FS-Data-Deduplication, the three usage types and their policies, Enable-DedupVolume -UsageType, Start-DedupJob -Memory, the NTFS and 2 GB limits from the cmdlet reference, ReFS support from Windows Server 2019, 64 TB volume support, the memory guidance, and that Disable-DedupVolume leaves data deduplicated. Removed the unconfirmed boot-volume, Exchange, 4 TB file size and antivirus claims.

Method: documentation only; no commands were run.
