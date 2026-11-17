---
id: computing-software.systems-network-administration.windows-server.dfsr-health-backlog-and-conflicts
name: dfsr-health-backlog-and-conflicts
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs-replication, dfsr-backlog, get-dfsrbacklog, conflictanddeleted, dfsr-health-report, write-dfsrhealthreport, dirty-shutdown, event-2213, dfsrdiag, get-dfsrstate]
level: practitioner
status: docs-checked
description: "Keep DFSR healthy: backlog monitoring, health reports, recovering conflicted/deleted files from ConflictAndDeleted, and dirty-shutdown (2213) recovery."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/get-dfsrbacklog
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/write-dfsrhealthreport
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/get-dfsrpreservedfiles
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/restore-dfsrpreservedfiles
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-faq
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DFSR health, backlog and conflicts

## Backlog (files waiting to replicate)
```powershell
(Get-DfsrBacklog -GroupName 'RG-Software' -FolderName 'Software' -SourceComputerName fs01 -DestinationComputerName fs02 -Verbose 4>&1 |
  Select-String 'Backlog File Count')
Get-DfsrState -ComputerName fs02 | Group UpdateState      # in-flight work on a member
```
Only the first 100 files are listed; `-Verbose` shows the count of all backlogged updates.
A growing backlog = connection down, schedule/bandwidth throttle, staging too small, or a
member stuck (check its DFS Replication event log). Connectivity errors are logged there while the schedule is open.

## Health report
```powershell
Write-DfsrHealthReport -GroupName 'RG-Software' -ReferenceComputerName fs01 -MemberComputerName fs02 -Path '<REPORT_DIR>'
```
HTML report: backlogs, errors, sharing violations, staging and conflict stats.

## Conflicts and deletions
Losers of conflicts and remotely deleted files go to `<folder>\DfsrPrivate\ConflictAndDeleted`
(`ConflictAndDeletedQuotaInMB` default 4096 MB). Recover:
```powershell
Get-DfsrPreservedFiles -Path '<DATA_DRIVE>:\Software\DfsrPrivate\ConflictAndDeletedManifest.xml' | Select Path,PreservedName,PreservedTime
Restore-DfsrPreservedFiles -Path '<DATA_DRIVE>:\Software\DfsrPrivate\ConflictAndDeletedManifest.xml' -RestoreToOrigin
```

## Open files and sharing violations
Files held open for long periods (for example `.pst` and Access files) are not replicated until they are closed. Do not apply file system policy to replicated folders: it reapplies NTFS permissions at each Group Policy refresh and can cause sharing violations. A paging file on the volume makes replication fail with event 4312.

## Verify
- [ ] Backlog under your threshold on all connections (alert on it).
- [ ] No unresolved errors in the DFS Replication event log.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: `Get-DfsrBacklog` lists at most 100 files and `-Verbose` gives the full count; `Write-DfsrHealthReport`, `Get-DfsrPreservedFiles` and `Restore-DfsrPreservedFiles -RestoreToOrigin` parameters; `ConflictAndDeletedQuotaInMB` default 4096; conflicts keep the older copy in DfsrPrivate\ConflictAndDeleted; open `.pst`/Access files, file system policy and paging-file (event 4312) notes from the FAQ. Removed the dirty-shutdown event 2213 recovery (including the WMI command), the MaxOfflineTime and the 4012, 5002, 5008, 4302 and 4304 event descriptions, which the checked pages do not state.

Method: documentation only; no commands were run.
