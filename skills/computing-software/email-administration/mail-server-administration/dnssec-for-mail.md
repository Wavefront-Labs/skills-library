---
id: computing-software.email-administration.mail-server-administration.dnssec-for-mail
name: dnssec-for-mail
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dnssec-for-mail, dnssec, dnssec-validation, ds-record]
level: advanced
status: draft
description: "Sign the zone and validate DNSSEC for mail: DS at the registrar, a local validating resolver, and key rollover cautions."
sources:
  - https://www.rfc-editor.org/rfc/rfc7672
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dnssec for mail

**Goal:** DANE and secure MX lookups depend on DNSSEC.
## Steps
1. Enable zone signing at your DNS host and add the DS record at the registrar.
2. Run a local validating resolver (unbound or similar) for the mail server; avoid forwarders that strip DNSSEC.
3. Check with `delv example.com MX` and `dig +dnssec`.
## Failure modes
- Broken DS after provider migration makes the whole domain bogus: mail and web both fail.
- Short resolver timeouts causing SERVFAIL on large responses.
## Verify
- `delv @127.0.0.1 example.com MX` prints `fully validated`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
