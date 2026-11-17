---
id: computing-software.systems-network-administration.windows-server.export-share-definitions-and-permissions
name: export-share-definitions-and-permissions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [workload-migration, share-registry-export, file-server, smb-shares, robocopy]
level: practitioner
status: docs-checked
description: "Move SMB share definitions and share permissions to a new file server: Get-SmbShare and Get-SmbShareAccess export, New-SmbShare recreate, data with robocopy."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbshare
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Exporting share definitions and permissions

robocopy copies files and, with `/copy:S` or `/copyall`, NTFS ACLs; it does not create the shares.
Export the share definitions and share-level permissions with PowerShell (this also lets you change paths).

## Export on the source
```powershell
Get-SmbShare -Special $false | Where-Object Name -notmatch '^(ADMIN|IPC|[A-Z])\$$' | ForEach-Object {
  [pscustomobject]@{Name=$_.Name;Path=$_.Path;Description=$_.Description;ABE=$_.FolderEnumerationMode;Caching=$_.CachingMode
    Access=(Get-SmbShareAccess $_.Name | ForEach-Object { "$($_.AccountName)|$($_.AccessRight)" }) -join ';'} } |
  Export-Csv shares.csv -NoTypeInformation
```
Recreate on the target:
```powershell
Import-Csv shares.csv | ForEach-Object {
  New-SmbShare -Name $_.Name -Path ($_.Path -replace '^D:', 'E:') -Description $_.Description -FolderEnumerationMode $_.ABE -CachingMode $_.Caching
  foreach ($a in $_.Access -split ';') { $n,$r = $a -split '\|'; Grant-SmbShareAccess -Name $_.Name -AccountName $n -AccessRight $r -Force } }
```

## Order of work
1. Robocopy data with `/copyall /mir` (`/copyall` equals `/copy:DATSOU`; `/mir` is `/e` plus `/purge`, so it deletes files at the destination that are not in the source). Run a first pass live and a final pass during cutover.
2. Create shares on the target.
3. Cut over (DNS alias or DFS target).

## Verify
- [ ] Share list and share permissions identical (`Get-SmbShareAccess` diff); users reach shares by the old name.

## Checked
2026-10-28. Confirmed against the Learn reference pages for `Get-SmbShare` (`-Special`, `-FolderEnumerationMode`, `-CachingMode`), `New-SmbShare` (`-Description`, `-FolderEnumerationMode` AccessBased/Unrestricted, `-CachingMode`), `Grant-SmbShareAccess` (`-AccountName`, `-AccessRight` Full/Change/Read, `-Force`) and `robocopy` (`/copy` flags, `/copyall`, `/mir`). Removed as unconfirmed: the LanmanServer registry export/import method and `net stop server` step, and the Storage Migration Service claim.
Method: documentation only; no commands were run.
