---
id: computing-software.email-administration.mail-server-administration.spf-record-authoring
name: spf-record-authoring
category: computing-software
field: email-administration
product: mail-server-administration
tags: [spf-record-authoring, spf, spf-record, txt, ip4, include]
level: practitioner
status: docs-checked
description: "Write a correct SPF TXT record for your domain with ip4/ip6, include, mx and a final -all or ~all."
sources:
  - https://www.rfc-editor.org/rfc/rfc7208
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spf record authoring

**Goal:** declare the hosts allowed to send for your envelope domain (RFC 7208).
## Steps
1. Publish one TXT: `example.com. TXT "v=spf1 mx ip4:192.0.2.25 include:_spf.vendor.example -all"`.
2. Only one SPF record per name; if a lookup returns more than one record, `check_host()` returns `permerror`.
3. Also publish SPF for the host name used in HELO/EHLO. The RFC's standard record for a host involved in mail processing is `relay.example.com. IN TXT "v=spf1 a -all"`. This matters most for bounces, where the MAIL FROM is null and only the HELO identity can be checked.
4. End the record with an `all` mechanism. The qualifiers are `+` pass, `-` fail, `~` softfail and `?` neutral. A softfail is a weak statement that the host is probably not authorized; `-all` is an explicit statement that it is not.
## Failure modes
- `v=spf1 +all` makes any address pass, so it offers no protection.
- Splitting a record is not allowed by publishing two TXT records (see step 2); one record can be composed of more than one string.
## Verify
- `dig +short TXT example.com` shows exactly one `v=spf1` string.
- Send to a test mailbox and read the SPF result the receiving server records in its headers.

## Checked

2026-11-09. Confirmed on RFC 7208: one record only (permerror on more than one), the null MAIL FROM and HELO identity guidance and the `v=spf1 a -all` host record (deployment section), qualifier list and the softfail and fail definitions, and the `v=spf1 +all` example where any address passes. Removed: the advice to start with ~all and later move to -all, the claim about `?all`, the missing-includes warning and the Authentication-Results spf=pass check, none of which the RFC states.

Method: documentation only; no commands were run.
