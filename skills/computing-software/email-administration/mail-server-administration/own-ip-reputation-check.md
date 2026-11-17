---
id: computing-software.email-administration.mail-server-administration.own-ip-reputation-check
name: own-ip-reputation-check
category: computing-software
field: email-administration
product: mail-server-administration
tags: [own-ip-reputation-check, ip-reputation, postmaster-tools, reputation-check]
level: practitioner
status: draft
description: "Check your sending IP and domain reputation across blocklists and provider postmaster tools regularly."
sources:
  - https://www.m3aawg.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Own ip reputation check

**Goal:** notice problems before recipients do.
## Steps
1. Check the IP on a handful of well-known blocklists with a script that loops `dig` queries.
2. Register your domain in Google Postmaster Tools and Microsoft's sender support portal (names and availability may change; confirm).
3. Watch for rising deferrals (`status=deferred` with `4.7.x`) in the mail log.
4. Record results weekly.
## Failure modes
- Checking only the IP and ignoring the domain: domain-level blocklists exist.
## Verify
- All checks return not listed; deferral rate to the big providers stays near zero.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
