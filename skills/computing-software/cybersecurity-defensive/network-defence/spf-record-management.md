---
id: computing-software.cybersecurity-defensive.network-defence.spf-record-management
name: spf-record-management
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, spf, sender-policy-framework, dns-txt, dns-lookup-limit, include-mechanism, spf-flattening, softfail, hardfail]
level: practitioner
status: docs-checked
description: "Publish and maintain SPF records: inventory senders, stay under the 10-lookup limit, choose ~all vs -all, protect non-sending domains and test changes."
sources: ["https://datatracker.ietf.org/doc/html/rfc7208", "https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure", "https://datatracker.ietf.org/doc/html/rfc7489"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPF record management

**Goal:** receivers can tell which servers may send mail as your domain's envelope sender, as
the foundation for DMARC.

## Build the record
1. Inventory every system that sends as your domain: mail platform (Microsoft 365, Google),
   marketing platforms, ticketing, HR, invoicing, on-prem relays. Use DMARC
   aggregate reports to find senders you missed.
2. Publish one TXT record at the domain apex:
```
example.com. TXT "v=spf1 include:spf.protection.outlook.com ip4:203.0.113.25 -all"
```
3. Prefer subdomains for third-party bulk senders (`news.example.com`) so each has its own SPF and reputation.

## Rules
- **10 DNS-lookup limit** (RFC 7208: at most 10 mechanisms and modifiers that cause DNS lookups, counting nested includes). Exceeding it gives `permerror`.
- Only one SPF record per name; two records = permerror.
- Avoid `ptr` (deprecated, slow) and `+all` (allows anyone).
- `~all` (softfail) vs `-all` (fail): with DMARC enforcing, either works; `-all` is clearer once the inventory is complete.
- Flattening (replacing includes by IPs) avoids the limit but breaks when providers change IPs; prefer subdomains.

## Non-sending domains
Parked and unused domains:
```
parked.example. TXT "v=spf1 -all"
_dmarc.parked.example. TXT "v=DMARC1; p=reject;"
```

## Gotchas
- SPF checks the envelope sender (Return-Path), not the visible From; that is why DMARC alignment matters.
- Forwarding breaks SPF; DKIM survives forwarding, so rely on both.

## Verify
- [ ] A DNS TXT query for the domain shows one SPF record; lookup count is 10 or fewer.
- [ ] Test message from each sender shows `spf=pass` in received headers (Authentication-Results).

## Checked

2026-10-28. Confirmed against: RFC 7208 (10-lookup limit, permerror, ptr, single record); Microsoft Learn 'Set up SPF in Microsoft 365' (spf.protection.outlook.com include); RFC 7489 (DMARC record).

Removed as unconfirmed: SendGrid include, CompTIA and M3AAWG sources, wildcard DKIM null-key record, 255-character TXT note.

Method: documentation only; no commands were run.
