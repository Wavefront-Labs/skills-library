---
id: computing-software.systems-network-administration.dns-dhcp.spf-record-design
name: spf-record-design
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, email-authentication, spf, txt, sender-policy-framework, dns-lookup-limit, include, softfail, hardfail, spf-flattening, envelope-from, permerror, email-dns]
level: practitioner
status: verified
description: "Write SPF records that pass: mechanism syntax, the 10-DNS-lookup limit and void lookups, -all vs ~all, one record per name, subdomains and testing with dig and mail headers."
sources:
  - https://datatracker.ietf.org/doc/html/rfc7208
  - https://www.m3aawg.org/sites/default/files/m3aawg-email-authentication-recommended-best-practices-09-2020.pdf
  - https://www.rfc-editor.org/rfc/rfc8601
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPF record design

SPF authorises IPs that may send mail using a domain in the **envelope sender** (MAIL FROM /
Return-Path), not the visible From header (that is DMARC's job).

## Syntax
```
example.org.  TXT  "v=spf1 ip4:198.51.100.0/28 ip6:2001:db8:25::/48 include:_spf.mailer.example include:spf.relay.example -all"
```
Mechanisms: `ip4`, `ip6`, `a`, `mx`, `include`, `exists`, `all`. Qualifiers: `+` pass (default),
`-` fail, `~` softfail, `?` neutral. Evaluated left to right; first match wins. (`ptr` also exists but is
not to be used, and `redirect` is a modifier.)

## Rules that break SPF
- **Exactly one** `v=spf1` TXT record per name. Two records = PermError.
- **10 DNS-lookup limit**: `include`, `a`, `mx`, `ptr`, `exists`, `redirect` each count (and
  nested includes count too). Over 10 = PermError (RFC 7208 section 4.6.4); `mx` may also not
  resolve more than 10 address records. `ip4`/`ip6`/`all` cost nothing.
- Void lookups (NXDOMAIN or empty answers): RFC 7208 section 4.6.4 says implementations SHOULD limit
  them to two, and exceeding the limit gives PermError.
- Strings > 255 characters must be split into multiple quoted strings within the same record:
  `"v=spf1 ... " "include:... -all"`. The strings are joined with no space added (RFC 7208 section
  3.3), so keep the space inside a string.
- `ptr` is headed "do not use" in RFC 7208 section 5.5: avoid it.

## Choosing -all vs ~all
`-all` once every sender is listed; `~all` while you are still inventorying senders. Domains that never send mail: `v=spf1 -all` plus DMARC `p=reject` and a null MX
(`MX 0 .`).

## Managing many senders
Inventory every system sending as your domain (M365/Google, marketing, CRM, ticketing, invoicing,
on-prem relays). Prefer giving third parties a **subdomain** (`mail.example.org`, `news.example.org`)
with its own SPF so the apex stays under the lookup limit. Flattening (replacing includes with IPs)
works but goes stale when providers change ranges: automate it if used.

## Test
```
dig +short TXT example.org | grep spf1
# count lookups with an SPF checker, or run pyspf (arguments: ip sender helo): python -m spf 198.51.100.5 bounce@example.org mx.example.org
```
pyspf 2.0.14 with a fake zone gave: two `v=spf1` records -> permerror ("Two or more type TXT spf records
found"); 11 `include:` terms -> permerror ("Too many DNS lookups"); 10 includes -> pass; 30 `ip4:` terms ->
pass. The `python -m spf` form above ran and returned `fail` for `example.org`, which publishes `-all`.
Received mail headers: `Received-SPF: pass` and `Authentication-Results: ... spf=pass smtp.mailfrom=example.org`.

## Verify
- [ ] Single SPF record, <= 10 lookups, all legitimate senders pass in headers.
- [ ] Non-sending domains/subdomains publish `v=spf1 -all`.
