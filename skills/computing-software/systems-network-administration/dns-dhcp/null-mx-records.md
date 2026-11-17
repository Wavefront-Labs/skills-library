---
id: computing-software.systems-network-administration.dns-dhcp.null-mx-records
name: null-mx-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, null-mx, rfc7505, mx-record, email]
level: practitioner
status: verified
description: "Publish a null MX (RFC 7505) for domains that receive no mail, its effect on senders and bounces, and conflicts with other MX records."
sources:
  - https://www.rfc-editor.org/rfc/rfc7505
  - https://www.rfc-editor.org/rfc/rfc5321#section-5.1
  - https://github.com/vdukhovni/postfix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null MX

Without any MX, SMTP falls back to the domain's A/AAAA record (implicit MX). A domain with a web
server but no mail service then receives delivery attempts it can never serve (RFC 7505).

## Record
```
example.com. IN MX 0 .
```
Exactly one MX, preference 0, exchange `.`. RFC 7505: a domain that advertises a null MX MUST NOT
advertise any other MX record.

## Effect
- Sending MTAs should fail immediately with a permanent error instead of queueing. Postfix's SMTP
  client bounces delivery to a null-MX domain rather than retrying (its source sets DSN status
  5.1.0). RFC 7505 recommends that a receiving server rejecting such a recipient use reply code 556
  with enhanced status 5.1.10 ("Recipient address has null MX").
- Receiving servers may reject messages whose envelope sender domain has a null MX (a bounce could
  never be delivered), reducing spoofing from that domain; RFC 7505 registers enhanced status 5.7.27
  for it. Postfix does this only if you use `reject_unknown_sender_domain` or
  `reject_unknown_recipient_domain` in your restrictions (they are not on by default); it then
  answers `550 5.7.27` (sender) or `556 5.1.10` (recipient) with `Domain example.com does not accept
  mail (nullMX)` (Postfix source, smtpd_check.c).

## Pair with
- `v=spf1 -all` and DMARC `p=reject` if the domain also sends no mail.
- Subdomains: null MX is per name; add it for each, or use a wildcard (`* IN MX 0 .`), which only
  covers names that have no records of their own (RFC 4592).

## Check
```
dig +short example.com MX
0 .
```
Confirmed against a local CoreDNS 1.15 zone containing `nomail IN MX 0 .`: dnspython parsed and
printed it back as `MX 0 .`.

## Gotchas
- Remove the null MX before onboarding mail; caches hold it for its TTL.

## Verify
- [ ] A test send to `test@example.com` fails immediately with a null MX permanent error, not a queued retry.
