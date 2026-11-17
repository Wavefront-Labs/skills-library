---
id: computing-software.cybersecurity-defensive.security-operations.m365-unified-audit-log
name: m365-unified-audit-log
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, unified-audit-log, m365, microsoft-purview-audit, search-unifiedauditlog, mailitemsaccessed, inbox-rules, business-email-compromise, entra-sign-in-logs]
level: advanced
status: docs-checked
description: "Investigate Microsoft 365 activity with the Unified Audit Log: search methods, key operations for BEC, MailItemsAccessed, retention limits and export."
sources: ["https://learn.microsoft.com/en-us/purview/audit-search", "https://learn.microsoft.com/en-us/powershell/module/exchange/search-unifiedauditlog", "https://learn.microsoft.com/en-us/purview/audit-log-retention-policies", "https://learn.microsoft.com/en-us/purview/audit-log-activities"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft 365 Unified Audit Log (UAL)

**Goal:** reconstruct what an account did across Exchange Online, SharePoint/OneDrive,
Teams and Entra ID during a suspected compromise.

## Access and retention
- Audit log search is on by default for Microsoft 365 and Office 365 enterprise organisations. Check in
  Exchange Online PowerShell (not Security & Compliance PowerShell, where the value is always False):
  `Get-AdminAuditLogConfig | Format-List UnifiedAuditLogIngestionEnabled`.
- Retention: 180 days for Audit (Standard) logs generated on or after 17 October 2023 (90 days before that).
  Users with an E5 licence (or the Purview Suite / E5 eDiscovery and Audit add-on) keep Entra ID, Exchange,
  SharePoint and OneDrive records one year by default; custom audit retention policies can extend this
  (up to 10 years with the add-on licence). Export early in an incident.
- Roles: Audit Logs or View-Only Audit Logs role in the Purview portal (and in Exchange admin center for the cmdlet).

## Search
Purview portal: Audit > Search (date range in UTC, maximum 180 days; users, activities, record types, keyword).
Search jobs keep running after the browser closes and are kept 30 days; up to 10 jobs at once per admin.
Broad jobs in large tenants can take up to 48 hours. Export to CSV is limited to 50,000 rows (Audit Standard)
or 1,000,000 rows (Audit Premium). PowerShell (Exchange Online module):
```powershell
Connect-ExchangeOnline
$r = Search-UnifiedAuditLog -StartDate 2026-10-01 -EndDate 2026-10-08 -UserIds user@contoso.com `
     -SessionId case123 -SessionCommand ReturnLargeSet -ResultSize 5000
```
By default the cmdlet returns up to 100 records; `-ResultSize` maximum is 5,000. Rerun with the same
`-SessionId` and `-SessionCommand` until no results come back. `ReturnLargeSet` pages up to 50,000 results,
unsorted; `ReturnNextPreviewPage` is sorted by date but limited to 5,000. Never switch between the two for one
session ID (output then limits to 10,000). Check `AuditSearchRequestMetadata.moreRecordsAvailable` to see
whether more remain. Microsoft recommends the Office 365 Management Activity API rather than a PowerShell script
for programmatic bulk download.

## Operations to check in a BEC or account takeover
| Operation | Why |
|---|---|
| `UserLoggedIn` (and Entra sign-in logs) | Source IPs, user agents, new countries |
| `New-InboxRule`, `Set-InboxRule` (Outlook on the web), `UpdateInboxRules` (Outlook client) | Rules that hide or forward replies |
| `Set-Mailbox` | Mailbox setting changes such as forwarding; read the `Parameters` in `AuditData` |
| `MailItemsAccessed` | Mail read: triggered when a mail client binds to messages or protocols such as Exchange ActiveSync or IMAP sync a folder |
| `Send`, `SendAs`, `SendOnBehalf` | Fraudulent emails |
| `Add-MailboxPermission`, `UpdateCalendarDelegation` | Persistence via delegated access (Add-MailboxPermission also fires for Microsoft system accounts doing maintenance) |
| `Add service principal`, `Add service principal credentials.`, `Add delegation entry.` | Application registration and permission grants (OAuth persistence) |
| `FileDownloaded`, `FileAccessed`, `AnonymousLinkCreated` | SharePoint/OneDrive data access |

Operation names must be entered exactly as the Audited activities page lists them; a misspelt name returns nothing.

## Parsing
`AuditData` is JSON: `$r | ForEach-Object { $_.AuditData | ConvertFrom-Json }` then select
`CreationTime, Operation, ClientIP, UserId, Parameters`. Normalise IPs (IPv6 and port suffixes).

## Gotchas
- Microsoft does not guarantee when a record appears; for core services (Exchange, SharePoint, OneDrive, Teams)
  it is typically 60 to 90 minutes, longer for other services. Do not conclude absence too early.
- Results are paged and capped; a single unpaged query silently truncates.
- Mailbox audit events for some users may be missing from portal and API searches even with mailbox auditing on by default.
- Restricted admins (scoped by administrative unit) cannot see some activities, for example Exchange `Set-Mailbox`; use an unrestricted admin.
- Entra sign-in logs have their own retention; check the current Entra retention page for your licence and stream them to a SIEM.

## Verify
- [ ] Full pull for the incident window completed (record counts per day) and stored with hashes.
- [ ] Inbox rules, forwarding, delegates and OAuth grants checked for every affected mailbox.

## Checked
Checked 2026-11-08 against Microsoft Learn: Search the audit log (Purview), Search-UnifiedAuditLog, Manage audit
log retention policies, Audited activities. Confirmed: ingestion check and its Exchange-only caveat, 180-day
Standard retention from 17 Oct 2023, E5 one-year default, 180-day search range, 50,000 / 1,000,000 export caps,
cmdlet defaults (100 records, ResultSize max 5,000, ReturnLargeSet 50,000 unsorted, ReturnNextPreviewPage 5,000),
session-mixing 10,000 limit, availability 60 to 90 minutes, operation names listed above. Removed as not found on
the pages: the 30 minutes to 24 hours delay, the 30-day Entra sign-in retention figure, MailItemsAccessed licence
claims, the ForwardingSmtpAddress parameter, "Consent to application", the Purview Audit Search Graph API, and the
CISA Untitled Goose Tool and Microsoft-Extractor-Suite mentions (not fetched). Operation `Send` and `SendAs` per
Audited activities.
Method: documentation only; no commands were run.
