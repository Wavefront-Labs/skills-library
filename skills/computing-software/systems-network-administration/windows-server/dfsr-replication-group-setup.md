---
id: computing-software.systems-network-administration.windows-server.dfsr-replication-group-setup
name: dfsr-replication-group-setup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs-replication, dfsr-staging, new-dfsreplicationgroup, new-dfsreplicatedfolder, add-dfsrmember, primary-member, initial-sync, preseeding, staging-quota, dfsr-module]
level: practitioner
status: docs-checked
description: "Set up DFS Replication between file servers: replication groups and folders in PowerShell, primary member and initial sync, preseeding with robocopy, and staging quota sizing."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfs-replication-overview
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/preseed-dfsr-with-robocopy
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-faq
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/set-dfsrmembership
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/new-dfsreplicationgroup
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/add-dfsrmember
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFS Replication group setup

**Use for:** read-mostly content to branches, hub-and-spoke collection, standby copies.
Not for files edited concurrently at several sites (no distributed locking: the version saved last wins and the other
is moved to DfsrPrivate\ConflictAndDeleted).

## Create
```powershell
Install-WindowsFeature FS-DFS-Replication -IncludeManagementTools    # on all members
New-DfsReplicationGroup -GroupName 'RG-Software' |
  New-DfsReplicatedFolder -FolderName 'Software' |
  Add-DfsrMember -ComputerName fs01,fs02
Add-DfsrConnection -GroupName 'RG-Software' -SourceComputerName fs01 -DestinationComputerName fs02
Set-DfsrMembership -GroupName 'RG-Software' -FolderName 'Software' -ComputerName fs01 `
  -ContentPath '<DATA_DRIVE>:\Software' -PrimaryMember $true -StagingPathQuotaInMB 32768 -Force
Set-DfsrMembership -GroupName 'RG-Software' -FolderName 'Software' -ComputerName fs02 `
  -ContentPath '<DATA_DRIVE>:\Software' -StagingPathQuotaInMB 32768 -Force
Update-DfsrConfigurationFromAD -ComputerName fs01,fs02
```
- **Primary member**: its copy wins during initial sync; differing files on other members are replaced, with the losing copies kept in the hidden `DfsrPrivate` folder. Choose the right primary.
- `-StagingPathQuotaInMB` and `-ConflictAndDeletedQuotaInMB` (default 4096) are set per membership.

## Preseed large data sets
Copy data first so initial sync only compares hashes:
```cmd
robocopy "\\fs01\d$\Software" "<DATA_DRIVE>:\Software" /E /B /COPYALL /R:6 /W:5 /MT:64 /XD DfsrPrivate /TEE /LOG+:preseed.log
```
Then verify hashes match with `Get-DfsrFileHash` on samples from both sides before creating the membership.

## Staging quota
Size the staging quota for the largest files in the folder; the cmdlet documentation uses 16384 to 32768 MB in its examples (`-StagingPathQuotaInMB`). Check the DFS Replication event log and the backlog if replication stalls.

## Verify
- [ ] Initial sync finished on each member; `Get-DfsrBacklog` near zero.
- [ ] A test file created on fs01 appears on fs02.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: the group creation pipeline cmdlets and `Add-DfsrConnection`/`Set-DfsrMembership` parameters (`-ContentPath`, `-PrimaryMember`, `-StagingPathQuotaInMB`, `-ConflictAndDeletedQuotaInMB` default 4096); last-saved wins and the other copy goes to DfsrPrivate\ConflictAndDeleted, no distributed locking (FAQ); the preseed Robocopy command; the 32768 MB and 16384 MB staging examples. Removed the 32-largest-files sizing rule and events 4104, 4202 and 4204, which the checked pages do not state.

Method: documentation only; no commands were run.
