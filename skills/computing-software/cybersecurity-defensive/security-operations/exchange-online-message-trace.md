---
id: computing-software.cybersecurity-defensive.security-operations.exchange-online-message-trace
name: exchange-online-message-trace
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, message-trace, exchange-online, get-messagetrace, phishing-investigation, emailevents, mail-flow, purge]
level: practitioner
status: docs-checked
description: "Trace email in Exchange Online for investigations: Get-MessageTraceV2, historical searches, EmailEvents in advanced hunting, finding all recipients of a phish, and purging."
sources: ["https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/message-trace-modern-eac", "https://learn.microsoft.com/en-us/powershell/module/exchange/get-messagetracev2", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exchange Online message trace

## Quick trace (up to 10 days of data per call)
```powershell
Connect-ExchangeOnline
Get-MessageTraceV2 -SenderAddress attacker@evil.example -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) |
  Select Received, SenderAddress, RecipientAddress, Subject, Status, MessageTraceId
Get-MessageTraceDetailV2 -MessageTraceId <id> -RecipientAddress user@corp.example   # hop-by-hop events
```
(`Get-MessageTraceV2` returns up to 1000 results by default, 5000 at most, within the last 90 days but only 10 days per query; with no parameters it returns the last 48 hours. Timestamps are UTC.)
- Filters: `-RecipientAddress`, `-Subject`, `-FromIP`, `-ToIP`, `-Status`.
- V2 has no pagination: query in rounds or narrow `-StartDate`/`-EndDate` for big searches.

## Older than 10 days (up to 90)
Exchange admin center > Mail flow > Message trace, date ranges up to 90 days, or a historical search report (see the message trace page); `Get-HistoricalSearch` returns the messages in a report.

## Defender for Office 365: advanced hunting
```kql
EmailEvents
| where Timestamp > ago(7d)
| where SenderFromAddress =~ "attacker@evil.example" or Subject has "Invoice overdue"
| project Timestamp, NetworkMessageId, SenderFromAddress, RecipientEmailAddress, Subject,
          DeliveryAction, DeliveryLocation, ThreatTypes
| join kind=leftouter (EmailUrlInfo | project NetworkMessageId, Url) on NetworkMessageId
| join kind=leftouter (UrlClickEvents | project NetworkMessageId, ClickUser=AccountUpn, ActionType) on NetworkMessageId
```
Gives recipients, URLs and who clicked (Safe Links) in one query. `EmailPostDeliveryEvents` shows
ZAP and manual remediations.

## Phishing workflow
1. From the reported message, take sender, subject, sending IP, URLs, attachment hashes.
2. Trace widely (same IP, similar subjects, sender domain) to find all recipients.
3. Clicks: UrlClickEvents / proxy logs; credential entry suspected -> identity response.
4. Remove: use your Defender for Office 365 remediation actions (see Microsoft's documentation for the current method).

## Gotchas
- Times are UTC.
- Internal-to-internal mail and mail sent by compromised accounts are traced the same way; check
  `-SenderAddress` for the victim to see what the attacker sent from their mailbox.

## Verify
Count recipients from the trace and confirm every delivered copy was handled by the remediation action.

## Checked

Date: 2026-10-28

- Confirmed in the message trace and cmdlet pages: 10 days of data per Get-MessageTraceV2 call within a 90 day range, default 48 hours with no parameters, 1000 default and 5000 maximum results, pagination deprecated in V2, UTC timestamps, parameters -FromIP and -Status, Subject filter supports contains, EAC report returns up to 20,000 results, EmailEvents/EmailUrlInfo/UrlClickEvents/EmailPostDeliveryEvents tables.
- Removed (not found): the older cmdlet deprecation wording, Status value list, historical search cmdlet and CSV timing, compliance search purge commands and portal purge path, distribution list note.
Method: documentation only; no commands were run.
