---
id: computing-software.digital-forensics-incident-response.incident-response-process.message-trace-phishing-scoping-and-purge
name: message-trace-phishing-scoping-and-purge
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [message-trace, email-purge, phishing, business-email-compromise, exchange-online, compliance-search, dfir]
level: practitioner
status: docs-checked
description: "Scope a phishing campaign with Exchange Online message trace, then remove the messages with a Content search and New-ComplianceSearchAction -Purge, within its documented limits."
sources: ["https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/message-trace-modern-eac", "https://learn.microsoft.com/en-us/purview/ediscovery-search-for-and-delete-email-messages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message trace, phishing scoping and purge

**Goal:** find every recipient of a malicious email and remove it from all mailboxes.

## Scope with message trace
```powershell
Connect-ExchangeOnline
Get-MessageTraceV2 -SenderAddress attacker@evil.example -StartDate (Get-Date).AddDays(-9) -EndDate (Get-Date) |
  Select Received,SenderAddress,RecipientAddress,Subject,Status,MessageTraceId
# Pivot on subject or sender domain if the attacker rotated addresses
Get-MessageTraceV2 -StartDate ... -EndDate ... | Where Subject -like "*Invoice 4471*"
```
- Get-MessageTraceV2 needs version 3.7.0 or later of the Exchange Online PowerShell V3 module.
- The Learn page says the time range can reach back 90 days, but you can query only 10 days of data at a
  time. Walk back in windows of 10 days or less. Older data needs `Start-HistoricalSearch`.
- Specify as many precise filters as you can (`SenderAddress`, narrow `StartDate`/`EndDate`). For a message sent to
  more than 1,000 recipients, `MessageTraceId` is required.
- Pipe a result into `Get-MessageTraceDetailV2` for the delivery events of one message.
- Client IP information is kept for 10 days and appears only in the Enhanced summary or Extended report.
- Click and delivery data (URL clicks, who opened what) come from your mail-security product; this skill does not
  document those tables.

## Identify impact
- Clickers: URL-click telemetry from your mail-security product, proxy logs, browser history.
- Credential entry: sign-ins from unusual IPs soon after a click; MFA prompts.
- Attachment execution: EDR process events on recipients' machines.

## Purge with Content search
The Learn page states: classic eDiscovery experiences were retired on 31 August 2025, and the page's
Compliance Search procedure applies only to Microsoft 365 operated by 21Vianet. Other tenants use the new eDiscovery
experience in the Microsoft Purview portal. It also recommends the "Remediate malicious email delivered in Office 365"
procedure over this one if you have Defender for Office 365 Plan 2. The cmdlet flow, as documented:
```powershell
$Search = New-ComplianceSearch -Name "IR-014 purge" -ExchangeLocation All -ContentMatchQuery '(From:attacker@evil.example) AND (Subject:"Invoice 4471")'
Start-ComplianceSearch -Identity $Search.Identity
New-ComplianceSearchAction -SearchName "IR-014 purge" -Purge -PurgeType HardDelete   # or SoftDelete
Get-ComplianceSearchAction   # status; the action is named "<search name>_Purge"
```
Documented limits and behaviour:
- Roles: Compliance Search role (or eDiscovery Manager) to search; Search And Purge role (Organization Management in
  Purview) to delete. Exchange Online Organization Management does not grant it; without the role
  `-Purge` fails with "A parameter cannot be found that matches parameter name 'Purge'".
- You must use Security & Compliance PowerShell.
- At most 10 items per mailbox can be removed at one time; it is an incident-response tool, not mailbox cleanup.
  Rerun if needed.
- Not supported on a mailbox with litigation hold or in-place hold: only 10 items are removed from the user's
  view, and those are not permanently deleted.
- At most 50,000 mailboxes in the search; above that the purge fails, even if fewer mailboxes have matches. Use
  search permissions filters to split the scope.
- Mailboxes and public folders only (not SharePoint or OneDrive); Teams items returned by the search are not deleted;
  unindexed items are not deleted.
- SoftDelete moves items to the Recoverable Items Deletions folder until the deleted item retention period ends.
  HardDelete moves them to Purges, inaccessible to the user, and they are removed later by the Managed Folder
  Assistant. Holds keep purged items until the hold expires.

## Gotchas
- Export a copy of one message (with headers) as evidence before purging.
- Internal forwards of the phish by users have a different sender; search by subject too.

## Verify
Rerun the search and compare the estimate (`Get-ComplianceSearch`): zero results. Block the sender, domain or URL
in your mail filter.

## Checked
2026-11-08. Confirmed against the two cited Learn pages: Get-MessageTraceV2 and Get-MessageTraceDetailV2 usage,
the 90-day range with 10 days per query, the 3.7.0 module requirement, MessageTraceId for over 1,000 recipients,
the 10-day client IP availability, and every purge limit, role and delete-type behaviour listed above. Corrected:
the old "V2 supports up to 90 days" wording; the classic eDiscovery retirement caveat added. Removed: Threat
Explorer, Safe Links, Advanced Hunting tables, Defender soft/hard-delete actions, Action Center and the Tenant
Allow/Block List (not on the cited pages).
Method: documentation only; no commands were run.
