---
id: computing-software.email-administration.mail-server-administration.ipv6-mail-setup
name: ipv6-mail-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [ipv6-mail-setup, ipv6-mail, ipv6, inet-protocols, aaaa, ip6-arpa]
level: advanced
status: draft
description: "Enable IPv6 for a mail server: AAAA, PTR in ip6.arpa, SPF ip6, and Postfix inet_protocols."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ipv6 mail setup

**Goal:** dual-stack mail without deliverability loss.
## Steps
1. `inet_protocols = all` (or `ipv4` to stay single-stack).
2. Add AAAA for the mail host and PTR in `ip6.arpa` using the documentation prefix style 2001:db8::25.
3. Add `ip6:2001:db8::25` to SPF.
4. Check blocklists for the IPv6 address and prefix; some operate on /64 ranges.
## Failure modes
- IPv6 without PTR or SPF: major providers may reject or spam-folder that traffic.
- Outbound prefers IPv6 when AAAA exists; `smtp_address_preference = ipv4` is an option.
## Verify
- `dig +short AAAA mail.example.com`; send a test over IPv6 and read the Received header.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
