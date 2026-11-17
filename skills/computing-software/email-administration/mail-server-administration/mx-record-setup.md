---
id: computing-software.email-administration.mail-server-administration.mx-record-setup
name: mx-record-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mx-record-setup, mail-dns-records, mx, mx-record, dns, dig]
level: practitioner
status: draft
description: "Publish MX records for a domain: hostnames not IPs, priorities, backup MX risks, and how to verify with dig."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mx record setup

**Goal:** senders find your inbound SMTP host via MX (RFC 5321 section 5).
## Steps
1. Create an A (and AAAA) record for the mail host, e.g. `mail.example.com. IN A 192.0.2.25`.
2. Publish `example.com. IN MX 10 mail.example.com.` (lower number = preferred). The target must be a hostname with address records and must not be a CNAME.
3. If a domain has no MX, senders fall back to its A/AAAA record (implicit MX); publish an explicit MX anyway.
4. Add a second MX only if that host applies the same recipient validation and spam policy; a weaker backup MX becomes the spammers' path.
## Failure modes
- MX pointing at a CNAME or an IP literal: some senders defer or bounce.
- Stale TTL after a cutover: lower the TTL a day earlier.
- Backup MX that accepts all recipients then bounces: causes backscatter.
## Verify
- `dig +short MX example.com` returns the expected priorities.
- `dig +short A mail.example.com` and `AAAA` resolve.
- `nc -v mail.example.com 25` shows a 220 banner.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
