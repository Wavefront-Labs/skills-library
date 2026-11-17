---
id: computing-software.digital-forensics-incident-response.incident-response-process.mailbox-access-scoping-with-mailitemsaccessed
name: mailbox-access-scoping-with-mailitemsaccessed
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [mailitemsaccessed, unified-audit-log, business-email-compromise, m365, data-access-scoping, dfir]
level: advanced
status: docs-checked
description: "Determine which emails an attacker read in Microsoft 365 using MailItemsAccessed audit events: sync vs bind, deduplication, and matching attacker sessions."
sources: ["https://learn.microsoft.com/en-us/purview/audit-log-investigate-accounts", "https://learn.microsoft.com/en-us/purview/audit-log-activities"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mailbox access scoping with MailItemsAccessed

**Goal:** answer the notification question "which messages did the attacker access?" with
evidence rather than assuming the whole mailbox.

## Prerequisites
- **MailItemsAccessed** is part of Audit (Standard) and of Exchange mailbox auditing, enabled by default for users with an
  Office 365 E3/E5 or Microsoft 365 E3/E5 license. For other licences, check the licensing guidance before relying
  on it, and confirm it was auditing during the incident window.
- It covers POP, IMAP, MAPI, EWS, Exchange ActiveSync and REST.
- Microsoft says to use the records after the breach is resolved and the actor evicted: identify the compromised
  mailboxes, the time frame, then search with `Search-UnifiedAuditLog`.

## Search
```powershell
Search-UnifiedAuditLog -StartDate 2026-09-01 -EndDate 2026-09-10 -UserIds jdoe@contoso.com `
  -Operations MailItemsAccessed -ResultSize 5000 | Export-Csv mia.csv -NoTypeInformation
```
(The Learn page's examples use `-ResultSize 1000`.) Filter on `AuditData` for `"MailAccessType","Value":"Sync"` or
`"Bind"`. Useful properties: `ClientIPAddress`, `ClientInfoString`, `SessionId`, `UserId`, `MailAccessType`,
`Folders`, `OperationCount`, and `InternetMessageId` per accessed message.

## Interpret
- **Sync**: recorded only when a mailbox is accessed by the desktop Outlook client for Windows or Mac, which
  downloads many items. One audit event is generated per folder, and all items in the synced folder are assumed
  compromised. Check each sync against the attacker's context (client IP address and protocol, via `ClientIPAddress`,
  `ClientInfoString`); if one matches, assume the whole mailbox was synced. A client that downloaded mail can read
  it offline later with nothing audited.
- **Bind**: an individual message access, recorded with its `InternetMessageId`. Binds within a 2-minute
  interval are aggregated into one record (`Folders` field in `AuditData`), with the count in `OperationCount`.
  Use the IDs to collect the messages and check them for sensitive content, or search the audit records for IDs of
  a few sensitive messages.
- **Deduplication**: duplicate bind records within an hour, and sync records at one-hour intervals, are filtered
  out unless one of `ClientIPAddress`, `ClientInfoString`, `ParentFolder`, `Logon_type`, `MailAccessType`,
  `MailboxUPN`, `User` or `SessionId` differs. Do not read the absence of repeats as absence of access.
- **Sessions**: `SessionId` separates attacker actions from the user's normal activity in the same mailbox.

## Also check
`Send` (sent, replied to or forwarded) and `SendAs` (sent using the SendAs permission), and `FileAccessed` in
SharePoint/OneDrive for attachments opened. `FileAccessed` is not logged again for the same user and file for five
minutes.

## Verify
Produce a table of message IDs accessed by attacker sessions, reconciled to a count, and
state explicitly any sync that forces a whole-folder or whole-mailbox assumption.

## Checked
2026-11-08. Confirmed on the Learn pages "Use MailItemsAccessed to investigate compromised accounts" and the audit
activities list: default licensing, protocols covered, sync and bind semantics, 2-minute aggregation, deduplication
rules and properties, the Search-UnifiedAuditLog usage, and the Send, SendAs and FileAccessed descriptions. Removed
(not on the pages): the claim about E5-only history, the AuditOwner check, 180-day retention, the throttling rule
(1,000 records per 24 hours) and `IsThrottled`, and `SearchQueryInitiatedExchange`.
Method: documentation only; no commands were run.
