---
id: computing-software.cybersecurity-defensive.security-operations.email-forensics
name: email-forensics
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [email-forensics, digital-forensics, email-headers, spf, dkim, dmarc, bec, message-trace, eml]
level: practitioner
status: draft
description: "Perform email forensics: header analysis (Received chain, SPF/DKIM/DMARC results), message IDs, mailbox audit and transport logs, and preserving messages as evidence."
sources: ["https://datatracker.ietf.org/doc/html/rfc5322", "https://learn.microsoft.com/en-us/purview/audit-mailbox", "https://datatracker.ietf.org/doc/html/rfc8601"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Email forensics

## Acquire properly
- Export original message as `.eml`/`.msg` (full headers and MIME), not forwarded copies (forwarding
  rewrites headers). In M365: Content search / eDiscovery export, or Threat Explorer download;
  Google Workspace: Vault export.
- Hash exported files (SHA-256) and log custody.

## Header analysis (read bottom-up)
- `Received:` headers: each hop prepends; the lowest trustworthy hop is the first one added by your
  own infrastructure. Everything below it is attacker-controllable.
- `Authentication-Results` (RFC 8601) from your gateway: `spf=pass/fail smtp.mailfrom=`,
  `dkim=pass header.d=`, `dmarc=pass header.from=`. Alignment matters: DKIM pass for
  `header.d=mailer.com` while From is `yourbank.com` is not alignment.
- `Return-Path` vs `From` vs `Reply-To` mismatch: classic BEC.
- `Message-ID` domain and format reveal sending software; use it to search for the same campaign.
- `X-Originating-IP`, `X-MS-Exchange-Organization-AuthAs`, `X-Mailer` when present.

## Body and attachments
Extract attachments (`ripmime`, `emldump.py`), hash them, analyse safely in a sandbox; extract URLs
and resolve redirect chains without clicking (sandbox or URL detonation service).

## Mailbox and transport evidence
- Message trace (M365 `Get-MessageTraceV2`, Google email log search) for all recipients of the campaign.
- Mailbox audit: `MailItemsAccessed` (what an attacker read in a compromised mailbox), inbox rules
  (`New-InboxRule`, `Set-InboxRule` in UAL) hiding replies, forwarding settings, OAuth app access.
- For BEC: sent items and deleted items recovery, conversation timeline with the counterparty.

## Gotchas
- Time zones differ per header; normalise to UTC.
- Gateways may rewrite URLs (Safe Links); decode to original.
- Journaling copies can differ from what the user saw.

## Verify
Report includes hashed original, decoded auth results with alignment verdict, delivery path, all
recipients, and actions taken by the user or attacker in the mailbox.
