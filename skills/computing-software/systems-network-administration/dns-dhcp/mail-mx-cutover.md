---
id: computing-software.systems-network-administration.dns-dhcp.mail-mx-cutover
name: mail-mx-cutover
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, mx-cutover, mx-record, email-migration, ttl]
level: practitioner
status: docs-checked
description: "Cut mail over to a new provider via MX changes: TTL lowering, SPF/DKIM/DMARC pre-staging, dual delivery, verifying inbound flow and rollback."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321#section-5
  - https://support.google.com/a/answer/140034
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mail MX cutover

Senders look up the MX records for the recipient domain to decide where to deliver (Google Workspace help). Cutover is a DNS change, so cached answers decide how long mail keeps going to the old system.

## Before the change (practitioner advice, days ahead)
1. Lower the MX record TTL well before the change, at least one old-TTL period ahead, so caches expire quickly at cutover.
2. Verify the domain with the new provider. Google requires verified domain ownership before Gmail activation.
3. Pre-stage sending authentication with the new provider: add its SPF include alongside the old one (mind the SPF DNS lookup limit), publish its DKIM selectors, and watch DMARC aggregate reports for the new sending source.
4. Create mailboxes and aliases on the new side and test delivery.

## Cutover
- Replace the old MX records rather than adding new ones next to them. RFC 5321 section 5.1: lower preference numbers are tried first, and a sender-SMTP must randomise MX records of equal preference to spread load, so equal-priority old and new records split mail between both systems.
- Google's Workspace page says to remove any other MX records because mail may not work correctly with old or incorrect ones left in place. Its current record is `smtp.google.com` with priority 1; accounts that started before 2023 may have legacy `aspmx` records, which still work.
- Wait for the change to take effect; Google states it can take up to 72 hours for new MX records to be recognised. Keep the old system accepting and forwarding mail until traffic stops (practitioner advice).

## Check (practitioner advice)
Query the MX records at your authoritative name server and at a public resolver, send test messages from external accounts, and watch the new provider's message trace and the old server's logs until traffic stops. Google also offers an Admin Toolbox Dig tool to compare published MX records with the expected values.

## After (practitioner advice)
- Remove the old SPF include and DKIM selectors once nothing sends from the old system.
- Raise the MX TTL back to your normal value.
- If a gateway sits in front, the MX points to the gateway and only its delivery target changes.

## Verify
- [ ] External test messages arrive at the new provider, the old server receives nothing new after the old TTL, and DMARC reports show aligned passes.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Google Workspace "Set up MX records" page in full and the RFC 5321 section 5.1 MX-selection text (preference order, randomise equal preference). Removed as unsupported: specific SPF include strings, Microsoft 365 selector names and MX hostnames, onmail.microsoft.com test address, the 300 s and 3600 s TTL values, and dig/swaks commands. Pre- and post-cutover steps are practitioner advice.
