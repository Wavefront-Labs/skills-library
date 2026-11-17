---
id: computing-software.cybersecurity-defensive.security-operations.phishing-email-triage
name: phishing-email-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [alert-triage, phishing-triage, email-headers, url-analysis, mailbox-purge, soc, user-reported-phishing]
level: practitioner
status: docs-checked
description: "Triage a user-reported phishing email: header and authentication analysis, safe URL and attachment checks, scoping recipients, purge and credential response."
sources: ["https://learn.microsoft.com/en-us/defender-office-365/threat-explorer-real-time-detections-about", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-urlclickevents-table", "https://datatracker.ietf.org/doc/html/rfc8601"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reported phishing email triage

**Goal:** decide within minutes whether a reported email is malicious, find everyone who
got it, remove it, and catch anyone who clicked or entered credentials.

## 1. Get the original
Work from the original message as an attachment (.eml/.msg) or from the mail platform
(Defender Threat Explorer), never a forwarded copy which loses headers. Open it in an
isolated analysis VM or read the raw source.

## 2. Headers
- `Authentication-Results` (RFC 8601): the receiving server records its check results, for
  example `spf=pass smtp.mailfrom=example.net`. A failure on a domain that should pass is a
  strong indicator. Pass does not mean safe; attackers own look-alike domains with perfect
  authentication.
- `From` display name vs address vs the envelope sender (`Return-Path`); a mismatch is worth
  noting. Check the first external `Received` hop, the sending IP and its reputation.
- Domain age of sender and link domains: days old is suspicious.

## 3. Content and payload
- URLs: extract (do not click), defang in notes. Unwrap safe-link rewrites. Detonate in a
  sandbox; look for credential-harvest pages impersonating a service the user trusts.
- Attachments: hash and look up; detonate unknowns in a sandbox.
- QR codes: decode the URL offline.
- BEC with no payload: payment change, gift card or urgent wire request; verify by a known
  phone number, not the email.

## 4. Scope
Search the mail logs for the same sender, subject, URL or attachment hash across all
mailboxes (Explorer / message trace / `EmailEvents` in KQL). Count delivered, junked,
quarantined. Then check click data (`UrlClickEvents`) and proxy logs for the URL domain.

## 5. Respond
- Purge all copies, block sender/domain/URL/hash in
  the mail gateway and web proxy.
- Clicked + entered credentials: reset password, revoke sessions/refresh tokens, review MFA
  methods added, inbox rules and OAuth consents for that user, check sign-ins after the click.
- Attachment opened: EDR scan/isolation decision on that endpoint.
- Reply to the reporter with the verdict (it drives future reporting).

## Gotchas
- Purging before scoping destroys evidence; export a sample first.
- Simulation emails from your own awareness platform: allowlist and auto-close them.

## Verify
After purge, a message trace search for the indicators returns no items in inboxes, and
every user who clicked has a documented follow-up.

## Checked
2026-11-09. Read: RFC 8601 (Authentication-Results header and example), Microsoft Learn Threat
Explorer page, and the advanced hunting EmailEvents and UrlClickEvents table pages (both tables
exist; EmailEvents has SenderFromAddress and a Return-Path/envelope sender field). Removed: the
CISA source (blocked, 403), `dmarc=` and Reply-To header detail, Google Workspace, URLScan and
VirusTotal named tools, the list of common attachment and lure types, IDN homograph note and WHOIS.
Method: documentation only; no commands were run.
