---
id: computing-software.systems-network-administration.dns-dhcp.mta-sts-and-tls-rpt
name: mta-sts-and-tls-rpt
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, email-authentication, mta-sts, tls-rpt, smtp-tls, starttls, mx, policy-file, well-known, dane, tlsa, email-dns]
level: practitioner
status: verified
description: "Enforce TLS for inbound mail with MTA-STS: _mta-sts TXT, the HTTPS policy file, testing to enforce, policy id changes, TLS-RPT reports and the DANE option."
sources:
  - https://datatracker.ietf.org/doc/html/rfc8461
  - https://datatracker.ietf.org/doc/html/rfc8460
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTA-STS and TLS-RPT

SMTP STARTTLS is opportunistic: an attacker can strip it or redirect MX lookups. MTA-STS lets a
domain declare "deliver to these MX hosts only over valid TLS".

## Three pieces
1. DNS TXT:
   ```
   _mta-sts.example.org. TXT "v=STSv1; id=20261016T1200"
   ```
   `id` is 1 to 32 letters or digits (RFC 8461 ABNF) and must uniquely identify each policy instance, so change it
   whenever the policy file changes (senders cache the policy up to max_age; ids have no implied ordering).
2. Policy file over HTTPS with a publicly trusted certificate at exactly
   `https://mta-sts.example.org/.well-known/mta-sts.txt`:
   ```
   version: STSv1
   mode: testing
   mx: mail.example.org
   mx: *.mail.protection.outlook.com
   max_age: 86400
   ```
   Content-Type `text/plain` (senders SHOULD check it; only `charset=utf-8` or `us-ascii` parameters matter), CRLF or
   LF line endings (the ABNF terminator is `LF / CRLF`), HTTP 200 only (redirects MUST NOT be followed), every MX
   hostname listed (a wildcard replaces the leftmost label as `*.example.net`). Host it on any static site (GitHub Pages, CDN, web server); cert must cover
   `mta-sts.example.org`.
3. TLS-RPT for reports:
   ```
   _smtp._tls.example.org. TXT "v=TLSRPTv1; rua=mailto:tlsrpt@example.org"
   ```
   Sending MTAs that support TLS-RPT send reports of TLS successes and failures (RFC 8460: JSON, normally daily, by
   email or HTTPS). Only `rua=` is required; if several TXT records exist, those not starting `v=TLSRPTv1;` are ignored.

## Rollout
- Start with `mode: testing` (senders report but still deliver). Review TLS-RPT for 2+ weeks:
  certificate name mismatches, expired certs, MX not listed.
- Switch to `mode: enforce`, increase `max_age` (RFC 8461's example uses 604800, one week; the maximum is
  31557600, one year), update `id`.
- When changing MX providers: add the new MX to the policy (and bump id) **before** changing MX
  records; remove old ones afterwards.
- `mode: none` + new id to withdraw.

## DANE alternative
DANE (TLSA records at `_25._tcp.mail.example.org`) needs DNSSEC on the zone holding the MX and TLSA records (see
dane-for-smtp); Microsoft documents inbound SMTP DANE for Exchange Online. MTA-STS needs no DNSSEC. Both can coexist.

## Verify
```
dig +short TXT _mta-sts.example.org
curl -sv https://mta-sts.example.org/.well-known/mta-sts.txt
```
- [ ] Policy fetches with a valid cert; all MX match the `mx:` lines and present valid certs for their names.
- [ ] TLS-RPT reports show no failures before moving to enforce.
