---
id: computing-software.systems-network-administration.windows-server.dfsr-preseeding-and-database-cloning
name: dfsr-preseeding-and-database-cloning
category: computing-software
field: systems-network-administration
product: windows-server
tags: [dfs-replication, dfsr-preseeding, dfsr-database-cloning, robocopy, initial-sync]
level: advanced
status: docs-checked
description: "Speed DFSR initial sync for large data: preseed with robocopy preserving hashes, verify with Get-DfsrFileHash, and export/import the DFSR database."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/preseed-dfsr-with-robocopy
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-faq
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/export-dfsrclone
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/import-dfsrclone
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/get-dfsrfilehash
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFSR preseeding and database cloning

Initial sync over the WAN of terabytes takes weeks and every file goes through staging. Preseeding copies the data
first so DFSR only has to compare hashes.

## Preseed with robocopy
Copy with identical ACLs and attributes so the file hashes match:
```cmd
robocopy "\\SRC01\D$\Data" "<DATA_VOLUME>\Data" /E /B /COPYALL /R:6 /W:5 /MT:64 /XD DfsrPrivate /TEE /LOG:preseed.log /V
```
- `/COPYALL` copies data, attributes, timestamps, the NTFS ACL, owner and auditing information; `/B` uses backup mode; `/XD DfsrPrivate` excludes the DfsrPrivate folder.
- The destination folder must not already exist on the destination server, and use the latest Robocopy version.

## Verify hashes
```powershell
Get-DfsrFileHash \\SRC01\D$\Data\Finance\* | Select-Object -First 5
Get-DfsrFileHash <DATA_VOLUME>\Data\Finance\*            | Select-Object -First 5
```
Compare hashes for files and folders (`Get-DfsrFileHash` or `Dfsrdiag`). Mismatched hashes mean the preseeded copy differs, for example in ACLs or attributes, and DFSR will replicate those files again.

## Database cloning, the fastest
DFSR keeps one database per volume holding all replicated folders on it. `Export-DfsrClone` and `Import-DfsrClone` clone it to another server (not supported for SYSVOL or read-only replicas in Windows Server 2012 R2):
```powershell
# on the source (upstream) server
Export-DfsrClone -Volume D: -Path <DATA_VOLUME>\DfsrClone
# copy files (robocopy as above) and the clone folder to the new server, then:
Import-DfsrClone -Volume D: -Path <DATA_VOLUME>\DfsrClone
```
Replication stops on the volume during the export; use `Get-DfsrCloneState` or DFSR event 2402 to see when the export has succeeded. Then add the new server as a member; it starts with a database and skips initial sync for unchanged files.

## Gotchas
- DFSR supports NTFS volumes only (not ReFS or FAT).
- Replication on the source volume stops until the export finishes.

## Verify
- [ ] After adding the member: initial sync completes quickly and the backlog is near zero (`Get-DfsrBacklog`).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: the Robocopy command and flags (`/e /b /copyall /r:6 /w:5 /MT:64 /xd DfsrPrivate /tee /log /v`) and their explanations; destination folder must not pre-exist; hash validation with `Get-DfsrFileHash` or `Dfsrdiag`; one database per volume; replication stops during `Export-DfsrClone` and event 2402 or `Get-DfsrCloneState` shows completion; clone not supported for SYSVOL or read-only replicas on Windows Server 2012 R2; NTFS-only support (FAQ). Removed event 2404 and 4104, the antivirus remark and the identical-relative-path rule, which the checked pages do not state.

Method: documentation only; no commands were run.
