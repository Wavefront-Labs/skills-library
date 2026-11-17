---
id: computing-software.systems-network-administration.windows-server.dfsr-authoritative-and-non-authoritative-sync
name: dfsr-authoritative-and-non-authoritative-sync
category: computing-software
field: systems-network-administration
product: windows-server
tags: [dfs-replication, dfsr-authoritative-sync, dfsr, msdfsr-options, conflictanddeleted]
level: advanced
status: docs-checked
description: "Force DFSR authoritative or non-authoritative resync of a replicated folder (non-SYSVOL) with msDFSR-Options and msDFSR-Enabled, step by step."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/set-dfsrmembership
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/update-dfsrconfigurationfromad
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-faq
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DFSR authoritative and non-authoritative sync (data folders)

Use when a member has diverged (for example restored from backup or with a damaged database).

## Non-authoritative: rebuild one member from its partners
```powershell
Set-DfsrMembership -GroupName RG-Data -FolderName Data -ComputerName FS02 -DisableMembership $true -Force
Update-DfsrConfigurationFromAD -ComputerName FS02
# wait until the DFS Replication event log shows the folder removed from FS02
Set-DfsrMembership -GroupName RG-Data -FolderName Data -ComputerName FS02 -DisableMembership $false -Force
Update-DfsrConfigurationFromAD -ComputerName FS02
```
FS02 then performs an initial sync; files that differ on FS02 lose and the losing copies are kept in the hidden `DfsrPrivate` folder (`PreExisting` or `ConflictAndDeleted`).

## Authoritative: make one member the source of truth
```powershell
# on all other members: disable
Set-DfsrMembership -GroupName RG-Data -FolderName Data -ComputerName FS02,FS03 -DisableMembership $true -Force
# on the authoritative member: mark primary
Set-DfsrMembership -GroupName RG-Data -FolderName Data -ComputerName FS01 -PrimaryMember $true -Force
Update-DfsrConfigurationFromAD -ComputerName FS01,FS02,FS03
# re-enable others one at a time
Set-DfsrMembership -GroupName RG-Data -FolderName Data -ComputerName FS02 -DisableMembership $false -Force
Update-DfsrConfigurationFromAD -ComputerName FS02
```
`-PrimaryMember` makes the member the primary for initial sync: it wins when copies differ. Confirm the setting afterwards with `Get-DfsrMembership`.

## Before you start
- Back up the data on every member; non-authoritative members lose local unique changes.
- Check the staging quota (`-StagingPathQuotaInMB`) is large enough for the largest files or initial sync crawls.

## Verify
- [ ] Backlog zero both directions (`Get-DfsrBacklog`); file counts match; PreExisting reviewed and cleaned.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: `Set-DfsrMembership` parameters `-DisableMembership`, `-PrimaryMember`, `-ContentPath`, `-StagingPathQuotaInMB` and `-Force`; `Update-DfsrConfigurationFromAD`; losing copies go to the hidden DfsrPrivate\ConflictAndDeleted folder (FAQ). Removed the 60-day offline cause, event IDs 4008, 4102, 4104 and 4112, the msDFSR-Options detail and the 32-file staging rule, none of which the checked pages state.

Method: documentation only; no commands were run.
