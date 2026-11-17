---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-file-server-migration
name: azure-file-sync-file-server-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-file-sync, azure-files-migration, server-migration, file-server, robocopy, namespace-migration, cutover]
level: advanced
status: docs-checked
description: "Migrate an on-premises file server to Azure Files using Azure File Sync: share mapping, in-place or new-server paths, robocopy catch-up and cutover."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/files/storage-files-migration-overview
  - https://learn.microsoft.com/en-us/azure/storage/files/storage-files-migration-robocopy
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Migrate a file server to Azure Files with Azure File Sync

## Plan share mapping
- Map existing shares to Azure file shares: one Windows Server (or cluster) can sync up to 30 Azure file shares.
  Below 30 shares a 1:1 mapping is recommended; above that, group shares as subfolders under a common folder that
  syncs to one Azure file share, or sync a volume root.
- Item counts: Microsoft tests 100 million items (files and folders) per share, but recommends keeping a single
  share below about 20-30 million for faster initial scan, restore and DR.
- Choose: **in-place** (install the agent on an existing Windows Server 2016 or newer) or a **new Windows Server**
  with the agent, then robocopy from the old server.

## New-server path
1. Deploy sync service, sync groups and empty Azure file shares.
2. New server: install agent, register, create server endpoints on empty folders,
   optionally enable cloud tiering so the local disk can be smaller than the data set.
3. Copy data from old server with robocopy, repeat until deltas are small:
```powershell
robocopy \\OLDFS\Finance '<vol>:\Shares\Finance' /MIR /COPY:DATSO /DCOPY:DAT /MT:16 /R:2 /W:1 /B /IT /XD 'System Volume Information' /UNILOG:<log-file>
```
4. Cutover: remove share access on the old server, final robocopy pass, create SMB
   shares with same names/permissions on the new server, move DNS alias or DFS-N target.

## Important
- Size the new server's volume and tiering policy for the copy wave; migrate in waves if it is small.
- Azure File Sync uploads from the server; watch upload progress before decommissioning.
- Share-level permissions: re-create SMB shares (`New-SmbShare`); NTFS ACLs travel with the data
  (`/COPY:DATSO` copies security and owner, `U` auditing information cannot be stored in an Azure file share).
- Do not use AzCopy sync for migration into an Azure file share: it does not remove files deleted at the source,
  unlike `robocopy /MIR`. Storage Migration Service is supported indirectly (mount the share on the target server).

## Verify
- [ ] Sync activity shows zero pending uploads per endpoint.
- [ ] Users access through the same UNC path after cutover.

## Checked
Date 2026-10-27. Documentation: Azure Files migration overview and robocopy guide, namespace mapping include,
Azure File Sync planning guide. Confirmed: 30 shares per server, 100 million tested items and the 20-30 million
guideline, robocopy flags and their meanings, AzCopy sync limitation, Storage Migration Service support.
Method: documentation only; no commands were run.
