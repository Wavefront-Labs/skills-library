---
id: computing-software.systems-network-administration.active-directory.ntds-dit-integrity-and-offline-defrag
name: ntds-dit-integrity-and-offline-defrag
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, ad-backup, ntds-dit, offline-defrag, esentutl, ntdsutil-files, semantic-database-analysis, ad-database-maintenance]
level: advanced
status: docs-checked
description: "Maintain the AD database offline: stop AD DS, check integrity with ntdsutil files and esentutl, semantic analysis, offline defrag to compact NTDS.dit, and move files."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/ad-database-offline-defragmentation
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Offline NTDS.dit integrity checks and defragmentation

Stop the Active Directory Domain Services service (or boot into Directory Services Restore Mode) before maintaining the
database. Back up first, and do one DC at a time with another DC online for logons.

## Check free space first
Online defragmentation runs as part of garbage collection (every 12 hours by default) but does not reduce the size of
Ntds.dit. Offline defrag creates a new, unfragmented file (and rebuilds indexes), which may be much smaller; it is worth it
only when the file is far larger than its content (for example after deleting many objects).

## Stop AD DS and check
```powershell
Stop-Service NTDS -Force
ntdsutil "activate instance ntds" files info quit quit
ntdsutil "activate instance ntds" files integrity quit quit
ntdsutil "activate instance ntds" "semantic database analysis" "go" quit quit
```
Semantic analysis checks the data against Active Directory semantics, unlike the files integrity check (ESE semantics);
its report is written to Dsdit.dmp.<n> in the current folder.

## Offline defrag
```powershell
New-Item '<vol>:\NTDSCompact' -ItemType Directory
ntdsutil "activate instance ntds" files "compact to <vol>:\NTDSCompact" quit quit
# then, as instructed by ntdsutil:
Copy-Item '<vol>:\NTDSCompact\ntds.dit' "$env:windir\NTDS\ntds.dit" -Force
Remove-Item "$env:windir\NTDS\*.log"
ntdsutil "activate instance ntds" files integrity quit quit
Start-Service NTDS
```
Keep a copy of the original ntds.dit until the DC has replicated successfully. If free space on the TEMP volume is
less than the compacted database, set TMP and TEMP to a volume with enough space; the target needs room for the new file.

## Move database or logs
`ntdsutil files "move DB to <path>"` / `"move logs to <path>"` to an existing folder, then restart the computer (the registry is
updated to the new location).

## Verify
- [ ] `Start-Service NTDS` succeeds, event 1000/1394 OK, `repadmin /showrepl` clean,
  `dcdiag /test:services` passes.
- [ ] ntds.dit size reduced as expected.

## Checked
2026-10-27, against the Learn articles "Perform offline defragmentation of the Active Directory database", "Use Ntdsutil to manage AD files" and "Complete a semantic database analysis" (SupportArticles-docs, current). Confirmed: back up first; stop AD DS or use DSRM; 12-hour online defrag that does not shrink the file; `compact to <dir>`; delete logs then copy the new file over the old; TMP/TEMP space requirement; files integrity check vs semantic analysis and Dsdit.dmp output; move DB/move logs with a restart; esentutl /r for recovery. Removed as unconfirmed: event 1646 and the garbage-collection diagnostics setting, esentutl /g, "go fixup", and the NTFS-permissions note.

Method: documentation only; no commands were run.
