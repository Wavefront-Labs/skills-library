---
id: computing-software.systems-network-administration.patch-management.wsus-database-maintenance-and-cleanup
name: wsus-database-maintenance-and-cleanup
category: computing-software
field: systems-network-administration
product: patch-management
tags: [windows-update-management, wsus, wsus-cleanup, susdb, wid, decline-superseded, iis-app-pool, reindex, patch-management, wsus-app-pool]
level: practitioner
status: docs-checked
description: "Keep WSUS healthy: decline superseded updates, run the cleanup wizard on a schedule, reindex SUSDB, tune the WsusPool app pool, and recover from a timing-out console."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/mem/configmgr/update-management/wsus-maintenance-guide
  - https://learn.microsoft.com/en-us/powershell/module/updateservices/invoke-wsusservercleanup
  - https://learn.microsoft.com/en-us/windows/deployment/update/windows-update-error-reference
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WSUS database maintenance and cleanup

**Goal:** a WSUS server whose console opens, whose clients scan quickly, and whose
database does not grow without bound.

## Routine (monthly, after the patch cycle)
1. **Decline superseded updates** that are no longer needed (after the superseding update
   is approved and deployed). Microsoft's maintenance guide lists declining superseded
   updates as its own step before the Cleanup Wizard; it also notes that some updates and
   revisions take 30 days to age out, so run the second manual cleanup 30 days after the first.
2. **Run cleanup**:
```powershell
Invoke-WsusServerCleanup -CleanupObsoleteComputers -CleanupObsoleteUpdates `
  -CleanupUnneededContentFiles -CompressUpdates -DeclineExpiredUpdates -DeclineSupersededUpdates
```
3. **Reindex SUSDB** with the T-SQL reindex script from Microsoft's maintenance guide (back up SUSDB first;
   create the optional custom indexes before the cleanup). Connect to a Windows Internal Database
   on Windows Server 2012 or later at `\\.\pipe\MICROSOFT##WID\tsql\query` (run SSMS as administrator);
   for SQL Server use the normal instance name.
4. Remove unused **products and classifications** (e.g. drivers, old OS versions, language
   packs not used): fewer updates = faster everything.

## IIS app pool (WsusPool)
Client errors 0x8024401C (HTTP 408, request timeout) and 0x80244022 (HTTP 503, service unavailable) can point to an overloaded WSUS web service. Check Microsoft's current WSUS guidance for app pool limits for your Windows Server version before changing them.

## When the console times out
Run cleanup steps one at a time from PowerShell (obsolete updates first is the heaviest
and may need several runs), reindex, then retry the console. In severe cases, use the
`spDeleteUpdate` stored procedure loop from the maintenance guide to delete obsolete
updates in batches.

## Gotchas
- With ConfigMgr, let the software update point maintenance options do decline/cleanup;
  don't double-manage.
- Downstream servers: start the cleanup at the bottom of the hierarchy and work up; servers in the same tier can be cleaned at the same time, but finish one tier before the next.
- Do not let ConfigMgr software update point syncs run during the maintenance.

## Verify
Console opens in seconds; `SUSDB` size and the count of non-declined updates drop after
cleanup; client scan times in `WindowsUpdate.log` are short; no 0x8024401c errors.

## Checked

Checked 2026-10-27 against Microsoft Learn: the WSUS maintenance guide (Configuration Manager troubleshooting), Invoke-WsusServerCleanup and the Windows Update error reference.
- `Invoke-WsusServerCleanup` parameters (-CleanupObsoleteComputers, -CleanupObsoleteUpdates, -CleanupUnneededContentFiles, -CompressUpdates, -DeclineExpiredUpdates, -DeclineSupersededUpdates): confirmed.
- Steps (backup, custom indexes, reindex, decline superseded, Cleanup Wizard), the 30-day aging note, the WID pipe name, the `spDeleteUpdate` batch script, ConfigMgr maintenance overlap: confirmed.
- Corrected: downstream cleanup order is bottom of the hierarchy first (the earlier "upstream first" was wrong).
- Removed unconfirmed: the WsusPool numeric settings, "reset server node", the sqlcmd file name, Express installation file advice.
Method: documentation only; no commands were run.
