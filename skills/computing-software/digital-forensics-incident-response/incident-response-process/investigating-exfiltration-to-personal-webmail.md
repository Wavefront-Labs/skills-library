---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-exfiltration-to-personal-webmail
name: investigating-exfiltration-to-personal-webmail
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [personal-email-exfiltration, insider-threat, data-exfiltration, webmail, dlp, dfir]
level: practitioner
status: draft
description: "Investigate insider exfiltration to personal webmail: forwarding and sent-to-self in mail logs, browser uploads to Gmail/Outlook.com, proxy and DLP evidence, and attachment reconstruction."
sources: ["https://learn.microsoft.com/en-us/purview/audit-log-activities", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceevents-table", "https://www.cisa.gov/topics/physical-security/insider-threat-mitigation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Investigating exfiltration to personal webmail

Two paths: the corporate mail system sends to a personal address (easy to prove from logs), or the user uploads files through a browser to Gmail/Outlook.com (needs endpoint, proxy or DLP evidence). Run under HR/Legal authorisation with need-to-know.

## Path 1: corporate mail to personal address
- Message trace / `EmailEvents`: `SenderFromAddress == user` and `RecipientEmailAddress` in consumer domains (gmail.com, outlook.com, icloud.com, proton.me) or the user's known personal address from HR records.
```kql
EmailEvents
| where SenderFromAddress =~ "user@corp.com" and EmailDirection == "Outbound"
| where RecipientEmailAddress has_any ("@gmail.com","@outlook.com","@hotmail.com","@icloud.com","@proton.me","@yahoo.")
| project Timestamp, RecipientEmailAddress, Subject, AttachmentCount, NetworkMessageId
| join kind=leftouter (EmailAttachmentInfo | project NetworkMessageId, FileName, FileSize, SHA256) on NetworkMessageId
```
- Auto-forwarding rules (`New-InboxRule`, `Set-Mailbox -ForwardingSmtpAddress`) in the unified audit log.
- Preserve the sent items via eDiscovery hold before the user can delete them.

## Path 2: browser upload to webmail
- Endpoint: Defender `DeviceEvents` with `ActionType == "BrowserLaunchedToOpenUrl"` is weak; better are DLP endpoint events (`FileUploadedToCloud`), file-access timelines (LNK, jump lists, Office MRU) showing the files opened just before.
- Proxy/SSE logs: POSTs to `mail.google.com`, `outlook.live.com` attachment upload endpoints with large request bytes; TLS inspection may give filenames.
- Browser history and cache on the host: compose URLs, attachment upload URLs, timing.
- Personal account login on a corporate browser profile (Chrome sync to a personal account) is itself evidence; check Chrome `Preferences` for signed-in accounts.

## Building the case
Correlate: file accessed (time) -> upload or send (time) -> size match. Tie the files to sensitivity labels or content review. Note timing relative to resignation or notice.

## Gotchas
- Personal mailbox contents are outside your reach; do not access them. Legal can seek them via litigation.
- Many users email work to themselves innocently; assess intent with HR, report facts not motives.

## Verify
Each exfiltration event in the report has a corroborating source (mail log plus attachment hash, or proxy plus endpoint file access) and an exact time.
