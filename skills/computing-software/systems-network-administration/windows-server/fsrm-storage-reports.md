---
id: computing-software.systems-network-administration.windows-server.fsrm-storage-reports
name: fsrm-storage-reports
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, fsrm, file-server-resource-manager, storage-reports, new-fsrmstoragereport, large-files, duplicate-files, least-recently-accessed, files-by-owner, capacity-planning]
level: practitioner
status: docs-checked
description: "Generate FSRM storage reports on demand or on schedule: large, duplicate, stale and per-owner files, file screen and quota usage, and acting on the results."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/storage-reports-management.md
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmstoragereport
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmscheduledtask
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/set-fsrmsetting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSRM storage reports

## Report types
The `-ReportType` values are LargeFiles, FilesByFileGroup, LeastRecentlyAccessed, MostRecentlyAccessed, QuotaUsage, FilesByOwner, DuplicateFiles, FileScreenAuditFiles and FilesByProperty.

## Scheduled report
```powershell
New-FsrmStorageReport -Name 'Monthly capacity' -Namespace @('<DATA_DRIVE>:\Shares') `
  -ReportType LargeFiles,DuplicateFiles,LeastRecentlyAccessed,FilesByOwner,QuotaUsage `
  -LargeFileMinimum 500MB -LeastAccessedMinimum 365 -ReportFormat DHtml,Csv `
  -Schedule (New-FsrmScheduledTask -Time (Get-Date '02:00') -Monthly 1) -MailTo 'storage-team@example.com'
Start-FsrmStorageReport -Name 'Monthly capacity'     # run now
Get-FsrmStorageReport | Select Name,LastRun,Status
```
Output locations for scheduled, on-demand and incident reports are set with `Set-FsrmSetting -ReportLocationScheduled`, `-ReportLocationOnDemand` and `-ReportLocationIncident`. `-ReportFormat` accepts DHtml, Html, Text, Csv and XML.

## Using the results
- **Large files** and **duplicates**: candidates for cleanup or dedup (the duplicates report identifies duplicate files so space can be reclaimed).
- **Least recently accessed**: archive candidates (`-LeastAccessedMinimum` is the number of days).
- **Files by owner**: chargeback/conversations with heavy users.

## Gotchas
- Reports on huge volumes can be slow and I/O heavy; schedule off-peak and limit namespaces.

## Verify
- [ ] Monthly report delivered; CSV output opens cleanly.
- [ ] Actions from the report (archive/delete) tracked with owners' agreement.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- New-FsrmStorageReport: -ReportType values (nine listed in the New-FsrmAction -ReportTypes enum), -LargeFileMinimum, -LeastAccessedMinimum, -ReportFormat (DHtml, Html, Text, Csv, XML), -MailTo, -Schedule with New-FsrmScheduledTask -Time ... -Monthly; Set-FsrmSetting -ReportLocationScheduled/-OnDemand/-Incident.
- storage-reports-management page: scheduled and on-demand reports, duplicate files report, Files by File Group and Files by Owner reports.
- Wrong claim fixed: "Folders by Property" is not a report type (FilesByProperty is). Removed unconfirmed details: default output folder paths, the last-access fsutil advice, Data Deduplication wording, and the NTFS owner remark.

Method: documentation only; no commands were run.
