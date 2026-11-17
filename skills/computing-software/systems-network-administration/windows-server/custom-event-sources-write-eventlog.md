---
id: computing-software.systems-network-administration.windows-server.custom-event-sources-write-eventlog
name: custom-event-sources-write-eventlog
category: computing-software
field: systems-network-administration
product: windows-server
tags: [event-logs, new-eventlog, write-eventlog, powershell, monitoring]
level: practitioner
status: docs-checked
description: "Write script and app events to the Windows event log: register sources with New-EventLog, write with Write-EventLog, entry types and event IDs."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-eventlog
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/write-eventlog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom event sources and Write-EventLog

Scripts that log to the event log get centralised by existing WEF/SIEM/monitoring pipelines for free.

## Register a source (once, elevated)
```powershell
New-EventLog -LogName Application -Source 'Ops-NightlyExport'
# or a dedicated log
New-EventLog -LogName 'Ops' -Source 'Ops-NightlyExport','Ops-CertCheck'
```
`-Source` accepts several names. Run `New-EventLog` from an elevated PowerShell (Run as administrator); for some
logs, writing events also needs administrator rights. The EventLog cmdlets work only on classic event logs; use
`Get-WinEvent` for the newer Windows Event Log logs.

## Write
```powershell
Write-EventLog -LogName Application -Source 'Ops-NightlyExport' -EventId 1000 -EntryType Information -Message 'Export started'
Write-EventLog -LogName Application -Source 'Ops-NightlyExport' -EventId 1901 -EntryType Error -Message "Export failed: $($_.Exception.Message)"
```
`-EventId` is required and its maximum is 65535. `-EntryType` accepts Error, Warning, Information, SuccessAudit and
FailureAudit (default Information). Pick an ID scheme and document it so alert rules can key on IDs.

## Verify
- [ ] `Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='Ops-NightlyExport'} -MaxEvents 5` returns entries.

## Checked
2026-10-28. Confirmed against the Learn reference pages for `New-EventLog` and `Write-EventLog`: parameters `-LogName`, `-Source` (string array), `-EventId` (required, max 65535), `-EntryType` values and default, admin requirement, classic-logs-only note. Removed as unconfirmed: `Limit-EventLog` example, the PowerShell 7 section (.NET EventLog calls, `eventcreate` ID range), the one-log-per-source rule, the missing-message-DLL note and the ID-range scheme.
Method: documentation only; no commands were run.
