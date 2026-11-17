---
id: computing-software.email-administration.mail-server-administration.reverse-dns-ptr
name: reverse-dns-ptr
category: computing-software
field: email-administration
product: mail-server-administration
tags: [reverse-dns-ptr, ptr, reverse-dns, rdns]
level: practitioner
status: draft
description: "Set and check PTR records for the mail server's outbound IPs so receivers' reverse-DNS checks pass."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reverse dns ptr

**Goal:** every IP that sends mail has a PTR record with a sensible hostname.
## Steps
1. PTR is controlled by whoever owns the IP block (your ISP or cloud provider), not by your own zone; request or set it in their portal.
2. Set the PTR to the mail host name, e.g. `25.2.0.192.in-addr.arpa. IN PTR mail.example.com.` (for 192.0.2.25).
3. Use the same name as Postfix `myhostname` and the SMTP HELO banner.
4. Do the same for IPv6 under `ip6.arpa`; one PTR per IP is the safe rule.
## Failure modes
- Generic provider PTR (dynamic-looking names) is often scored down or rejected by receivers.
- PTR name that does not resolve forward to the same IP (see forward-confirmed-rdns).
- Multiple PTR records on one IP: some checkers fail.
## Verify
- `dig +short -x 192.0.2.25` returns `mail.example.com.`
- `host mail.example.com` returns 192.0.2.25.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
