---
id: computing-software.systems-network-administration.windows-server.dfsr-schedules-bandwidth-and-file-filters
name: dfsr-schedules-bandwidth-and-file-filters
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs, dfsr-schedule, dfsr-file-filters, bandwidth-throttling, set-dfsrgroupschedule]
level: practitioner
status: docs-checked
description: "Set DFS Replication schedules and bandwidth limits per group or connection, and file and subfolder filters, with PowerShell and the gotchas of excluded files."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/set-dfsrgroupschedule
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/set-dfsrconnectionschedule
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/set-dfsreplicatedfolder
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFSR schedules, bandwidth and file filters

## Schedules
Replication group schedule applies to all connections unless a connection has a custom schedule.
```powershell
# replicate all the time, full bandwidth (default)
Set-DfsrGroupSchedule -GroupName 'Branch-Files' -ScheduleType Always
# business hours throttled to 16 Mbps, full speed out of hours: 96 hex digits per day, one per 15-minute block
$day = ('F' * 28) + ('A' * 44) + ('F' * 24)       # 0 = no replication, 1 = 16 Kbps ... A = 16 Mbps ... E = 256 Mbps, F = full bandwidth
Set-DfsrGroupSchedule -GroupName 'Branch-Files' -Day Monday,Tuesday,Wednesday,Thursday,Friday -BandwidthDetail $day
Get-DfsrGroupSchedule -GroupName 'Branch-Files'
# per connection
Set-DfsrConnectionSchedule -GroupName 'Branch-Files' -SourceComputerName FS-HQ -DestinationComputerName FS-BR1 -ScheduleType UseGroupSchedule
```
The GUI (DFS Management > replication group > Edit Replication Group Schedule) is easier for bandwidth grids.
`-UseUTC` chooses whether the schedule uses Coordinated Universal Time or the destination computer's local time. Bandwidth throttling is set per connection, is not 100% accurate, and DFSR performs no bandwidth sensing.

## File and subfolder filters
Filters take file names and wildcards (not paths). Files with the temporary attribute are never replicated.
```powershell
Set-DfsReplicatedFolder -GroupName 'Branch-Files' -FolderName Files -FileNameToExclude '~*','*.bak','*.tmp','*.pst'
Set-DfsReplicatedFolder -GroupName 'Branch-Files' -FolderName Files -DirectoryNameToExclude 'Scratch','.cache'
```

## Gotchas
- `.pst` and Access files stay open for long periods and are not replicated until closed, so excluding them is common.
- DFSR does not replicate the FILE_ATTRIBUTE_TEMPORARY attribute.
- Throttling too hard causes backlog growth; watch `Get-DfsrBacklog`.

## Verify
- [ ] Backlog drains during the full-speed window; excluded patterns do not appear on partners.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: `Set-DfsrGroupSchedule -BandwidthDetail` format (96 hexadecimal characters, 15-minute blocks, 0 to F with the documented mapping: A = 16 Mbps, 8 = 4 Mbps) and `-UseUTC`; `Set-DfsrConnectionSchedule` and `Set-DfsReplicatedFolder -FileNameToExclude/-DirectoryNameToExclude` parameters; throttling inaccuracy and no bandwidth sensing; `.pst`/Access files and the temporary attribute (FAQ). Corrected the bandwidth example (character 8 means 4 Mbps; A means 16 Mbps) and removed the default exclusion list and the fsutil/attribute-clearing commands, which the checked pages do not state.

Method: documentation only; no commands were run.
