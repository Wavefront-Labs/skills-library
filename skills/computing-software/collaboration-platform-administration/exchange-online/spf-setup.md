---
id: computing-software.collaboration-platform-administration.exchange-online.spf-setup
name: spf-setup
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [spf-setup, exo-email-authentication]
level: practitioner
status: draft
description: Publish a single valid SPF record covering Exchange Online and other senders.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPF record for Exchange Online
**Goal:** Publish a single valid SPF record covering Exchange Online and other senders.

- Record: `v=spf1 include:spf.protection.outlook.com -all` plus other senders' includes.
- Only one SPF TXT per domain; max 10 DNS lookups.
- Use `~all` while testing, `-all` when sure.
- Subdomains that send nothing: `v=spf1 -all`.

## Gotchas
- Exceeding 10 lookups gives PermError; flatten or remove unused includes.
- SPF breaks on forwarding; DKIM/DMARC cover that.

## Self-check
`nslookup -type=TXT <domain>` and a header check showing spf=pass.
