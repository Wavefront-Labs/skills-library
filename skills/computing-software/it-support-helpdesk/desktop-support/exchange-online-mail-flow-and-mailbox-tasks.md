---
id: computing-software.it-support-helpdesk.desktop-support.exchange-online-mail-flow-and-mailbox-tasks
name: exchange-online-mail-flow-and-mailbox-tasks
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, message-trace, email-quarantine, exchange-online]
level: practitioner
status: docs-checked
description: "Handle Exchange Online missing-mail tickets: run a message trace, read delivery statuses, and find and release quarantined messages from the Defender portal."
sources:
  - "https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/message-trace-modern-eac"
  - "https://learn.microsoft.com/en-us/defender-office-365/quarantine-admin-manage-messages-files"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# exchange-online-mail-flow-and-mailbox-tasks

## "I didn't get the email": message trace
- Exchange admin center (https://admin.exchange.microsoft.com) > Mail flow > **Message trace**, then
  Start a trace with sender, recipient and date range.
- The default time range is 2 days; ranges up to 90 days are allowed. For 10 days or less the Summary
  report is instant; you can query only 10 days of data at a time. Older data needs the
  `Start-HistoricalSearch` cmdlet in Exchange Online PowerShell (a downloadable report).
- PowerShell: `Get-MessageTraceV2` (needs Exchange Online PowerShell V3 module 3.7.0 or later), with
  `-StartDate` and `-EndDate`; pipe to `Get-MessageTraceDetailV2` for the events.
- Delivery statuses on the page: Delivered, Failed (not delivered), Pending (delivery being attempted
  or reattempted), Quarantined (as spam, bulk mail or phishing), Filtered as spam, Expanded (a distribution
  group was expanded to its members), Getting status (just received, check again in a few minutes).
- Delivered is "successfully delivered to the intended destination"; then look in the user's rules, Junk and other folders.

## Quarantine release
- Defender portal (https://security.microsoft.com) > Email & collaboration > Review > **Quarantine** > Email tab.
  Filters on the page include Quarantine reason; the last filters are cached.
- Reasons shown: Spam, Bulk, Phish, a mail flow (transport) rule, or Malware.
- Taking action on messages for all users needs membership in the Quarantine Administrator, Security
  Administrator or Organization Management role groups.
- Select the message to view, release, download or delete it. The Release action is not available for
  an already released message, and you cannot release to the same recipient more than once.
- You can submit an erroneously quarantined message to Microsoft as a false positive while releasing.
- Messages are deleted automatically after the date in the Expires column and are not recoverable;
  retention depends on why the message was quarantined.
- Use message trace to confirm a released message reached the Inbox; non-Microsoft anti-virus or
  outbound connectors can re-quarantine or strip released messages.
- Legitimate messages only: pass phishing or malware to security rather than releasing.

## Verify
The trace shows Delivered, or the released message arrives in the Inbox.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the message trace (EAC) and quarantine admin pages. Removed because the cited archive page
returned 404 and no other page was cited: archive and quota figures, OOF, forwarding, distribution list
and dynamic list claims, and unsupported status wording.
