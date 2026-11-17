---
id: computing-software.cloud-infrastructure-engineering.azure.migrate-file-servers-to-azure-files-with-robocopy
name: migrate-file-servers-to-azure-files-with-robocopy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-files, robocopy, file-server-migration, acl-preservation, cutover]
level: practitioner
status: docs-checked
description: "Migrate a Windows file server to Azure Files with RoboCopy: share planning, ACL-preserving copy flags, delta passes, cutover and when to use File Sync or Storage Mover instead."
sources: ["https://learn.microsoft.com/azure/storage/files/storage-files-migration-robocopy", "https://learn.microsoft.com/azure/storage/files/storage-files-migration-overview", "https://learn.microsoft.com/windows-server/administration/windows-commands/robocopy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate file servers to Azure Files with RoboCopy

**Goal:** move shares with data, timestamps and NTFS permissions intact and a short cutover window.

## Choose the method
- **RoboCopy** (this skill): direct to Azure file shares, users then map to Azure Files.
- **Azure File Sync**: keep a Windows cache on-prem, or seed and cut over gradually.
- **Azure Storage Mover**: managed, agent-based migrations at scale; **Data Box** for very large data / slow links.

## Prepare
1. Map source shares to Azure file shares (one share per volume/department; respect per-share size/IOPS targets).
2. Set up identity-based auth on the storage account and share-level permissions first.
3. Mount the target as an admin who can write ACLs (privileged role or storage key), on a machine near the source.

## Copy
```powershell
robocopy \\fs01\Finance Z:\ /MT:20 /R:2 /W:1 /B /MIR /IT /COPY:DATSO /DCOPY:DAT /NP /NFL /NDL `
  /XD "System Volume Information" /UNILOG:<LOG_DIR>\finance-pass1.log
```
- `/B` backup mode reads files regardless of ACLs (run elevated with backup privilege).
- `/COPY:DATSO` data, attributes, timestamps, security, owner; `/DCOPY:DAT` for directories.
- `/MIR` mirrors deletions - double-check source/target order before running.
- `/MT:n` threads: default 8; the Azure Files guide suggests 8-20 for a balanced initial copy. `/IT` preserves fidelity in mirror scenarios (for example an ACL change followed by an attribute change between runs).

## Delta passes and cutover
1. Run the same command repeatedly; each pass gets faster. Track duration of the last pass.
2. When the delta pass fits the window: stop user access (share permissions read-only or remove share),
   run the final pass, then repoint users (DFS-N target change, GPO drive maps, or DNS CNAME with SPN).
3. Keep the source read-only for rollback for a defined period.

## Gotchas
- Default share root ACLs on Azure Files are broad - set root ACLs before copying.
- Unsupported names and open files show as errors in the log - review the error lines.
- Throughput is limited by per-share and per-file targets and latency; parallel robocopy jobs across shares help.

## Verify
- [ ] Final pass log shows 0 failed; spot-check ACLs with `icacls` on the target; users open files via the new path.

## Checked

2026-10-28. Confirmed on the Azure Files RoboCopy migration page: the example flags (/MT, /R, /W, /B, /MIR, /IT, /COPY:DATSO, /DCOPY:DAT, /NP, /NFL, /NDL, /XD, /UNILOG), /MT default 8 and 8-20 guidance, /MIR deletion warning, /IT meaning. Removed: the 16-64 thread range, the 255-character path limit and the recycle-bin exclusion.

Method: documentation only; no commands were run.
