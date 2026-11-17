---
id: computing-software.systems-network-administration.windows-server.robocopy-file-migration-with-acls
name: robocopy-file-migration-with-acls
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, workload-migration, server-migration, robocopy, file-server-migration, ntfs-permissions, mir, backup-mode]
level: practitioner
status: docs-checked
description: "Copy file server data with robocopy preserving ACLs, owners and timestamps: initial seed and delta passes, exact flags, logging, exclusions and verifying results."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Copy file data with robocopy preserving ACLs

## The command
```powershell
robocopy \\OLDFS\Data$ '<vol>:\Data' /MIR /COPY:DATSOU /DCOPY:DAT /SECFIX /B /MT:32 /R:1 /W:1 `
  /XD '$RECYCLE.BIN' 'System Volume Information' 'DfsrPrivate' /XF 'thumbs.db' '~$*' `
  /NP /NFL /NDL /TEE /LOG+:'<vol>:\Logs\data.log'
```
| Flag | Why |
|---|---|
| `/MIR` | mirror: copy and delete extras at destination (dangerous if source and dest are swapped) |
| `/COPY:DATSOU` | data, attributes, timestamps, security (ACL), owner, auditing (SACL: needs Manage auditing right) |
| `/DCOPY:DAT` | directory timestamps too |
| `/SECFIX` | fixes security on all files, even skipped ones |
| `/B` | backup mode (needs backup/restore privileges; run elevated) |
| `/MT:32` | multithreaded (do not combine with `/IPG`) |
| `/R:1 /W:1` | default is 1,000,000 retries with a 30 s wait |
Use `/ZB` only for unreliable WAN links (restartable mode is slower).

## Strategy
1. Seed: run the full command days before cutover (copies the bulk).
2. Delta passes nightly: same command; only changes move. `/SECFIX` picks up ACL edits.
3. Cutover: make the source read-only (share permission Read), final pass, switch DNS
   alias/DFS-N target, recreate shares (`New-SmbShare` with the same permissions;
   record the source share permissions beforehand).

## Gotchas
- Local-group ACEs from the old server become orphaned SIDs on the new one; use domain groups.
- `/MIR` to the wrong destination root deletes data: test with `/L` (list only) first.
- Exit codes: Learn documents 0-7 as no failure (1 = all files copied) and any value of 8 or greater as at least one
  failure. Scripts must not treat non-zero as failure blindly.

## Verify
- [ ] Final log "Failed" column 0; spot-check ACLs with `icacls` on both sides;
  file/folder counts match (compare the summary of a `/L` list-only run).

## Checked
2026-10-28. Confirmed on Learn robocopy page: /copy flags (DATSOU equals "all file info"), /secfix, /dcopy, /b, /zb, /mir, /mt
(incompatible with /ipg), /r default 1,000,000 and /w default 30, /xd, /l, /np, /tee, /log+, exit codes 0-7 and 8+.
Removed as unconfirmed: SECFIX "later passes" wording, share-permission claim, long-path remark, SID requirement.
Method: documentation only; no commands were run.
