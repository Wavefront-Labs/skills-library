---
id: computing-software.digital-forensics-incident-response.evidence-handling.exporting-microsoft-365-evidence-with-purview
name: exporting-microsoft-365-evidence-with-purview
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [purview-ediscovery, m365, cloud-evidence, legal-hold, unified-audit-log, dfir]
level: practitioner
status: docs-checked
description: "Export Microsoft 365 evidence with Purview eDiscovery: cases, holds, searches, review sets and export, plus Audit search and CSV export, with custody records."
sources: ["https://learn.microsoft.com/en-us/purview/edisc", "https://learn.microsoft.com/en-us/purview/audit-search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting Microsoft 365 evidence with Purview

**Goal:** preserve and collect mailbox, file and chat content plus audit records for an investigation in a defensible way.

## Preserve first
- An eDiscovery case holds all searches, holds and review sets for one investigation, and you can assign members to control who sees the case. Place content locations on hold in the case: holds protect electronically stored information from inadvertent or intentional deletion during the investigation.
- Check for retention or deletion policies that could remove relevant content before the hold takes effect (Microsoft's pages cited here do not describe how they interact with holds, so confirm in your tenant).

## Collect
- eDiscovery searches mailboxes, OneDrive accounts, SharePoint sites, Teams, Microsoft 365 Groups and Viva Engage in the same search. Use search statistics to judge the items and relevance before exporting; searches are not immutable, even after results are added to a review set.
- Export copies items from their original location and packages them for download to a local computer; the export flow is unified across premium and non-premium features.
- Premium eDiscovery (requires an E5 subscription or related add-on) adds review sets, which are a secure Microsoft-provided Azure Storage location holding a static copy of the collected items you can search, filter and tag. It also adds conversation threading for Teams and Viva Engage chats, OCR, decryption of Microsoft-encrypted content, and external data import.
- Advanced indexing: when a search, review set or export runs, locations with partially indexed items are reindexed so those items become searchable.
- Role-based permissions control who can do eDiscovery tasks. Content Search functionality is now in a system-generated eDiscovery case available to members of the eDiscovery Manager and Administrator role groups.

## Audit evidence
Audit (Standard) and Audit (Premium) search the unified audit log in the Purview portal or with `Search-UnifiedAuditLog` (an Exchange Online cmdlet run in Exchange Online PowerShell).
- Date range is in UTC, defaults to the last seven days and has a maximum of 180 days; if you turn on auditing recently, the range cannot start before that date.
- Retention depends on the licence assigned to the user; for non-E5 licences records are retained for 180 days (Audit (Standard) logs from 17 October 2023 onward; earlier logs 90 days).
- The Export command exports search job items to a .csv file, up to 50,000 rows for Audit (Standard) and 1,000,000 rows for Audit (Premium). Access is scoped by the administrative units assigned to the admin.

## Custody
Record case name, search query text, locations, run time, item counts and export details, and hash every exported file when it is downloaded.

## Verify
Search statistics reconcile with the export, partially indexed items are accounted for, audit exports stayed under the row limit, and hashes are in the evidence log.

## Checked
Checked 2026-11-09 against the Microsoft Learn eDiscovery overview and the Audit search page (case, hold, search, export, review set and advanced indexing descriptions; audit date range, retention, cmdlet and CSV export limits). Removed: the `Set-Mailbox` litigation hold command, search KQL operators, export format claims (PST, .msg, .eml, HTML transcripts), Recoverable Items statements, the export tool download and large-export duration notes, and the claim that content access is itself audited.
Method: documentation only; no commands were run.
