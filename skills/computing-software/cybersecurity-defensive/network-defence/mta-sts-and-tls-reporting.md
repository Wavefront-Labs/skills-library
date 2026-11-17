---
id: computing-software.cybersecurity-defensive.network-defence.mta-sts-and-tls-reporting
name: mta-sts-and-tls-reporting
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, mta-sts, tls-rpt, smtp-tls, starttls-downgrade, dane, email-encryption-in-transit]
level: practitioner
status: docs-checked
description: "Enforce TLS for inbound mail with MTA-STS and receive TLS-RPT reports, or use DANE; publish policy, test mode first, and monitor failures."
sources: ["https://datatracker.ietf.org/doc/html/rfc8461", "https://datatracker.ietf.org/doc/html/rfc8460"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTA-STS and TLS reporting

**Goal:** mail sent to your domain is delivered only over authenticated TLS by senders that honour MTA-STS, preventing
STARTTLS stripping and MX spoofing by on-path attackers.

## MTA-STS setup
1. Host the policy at `https://mta-sts.example.com/.well-known/mta-sts.txt` with a valid public certificate:
```
version: STSv1
mode: testing
mx: mail.example.com
mx: *.example.net
max_age: 604800
```
2. Publish the DNS record (change `id` whenever the policy changes):
```
_mta-sts.example.com. TXT "v=STSv1; id=20261016T000000"
```
3. Publish TLS reporting:
```
_smtp._tls.example.com. TXT "v=TLSRPTv1; rua=mailto:tlsrpt@example.com"
```
4. Review TLS-RPT JSON reports for failures (certificate mismatch, expired certs, MX not in policy) while in testing mode.
5. Switch to `mode: enforce`, increase `max_age`, update `id`.

## Gotchas
- Policy host certificate expiry or a missing MX in the policy breaks inbound mail from enforcing senders: monitor both.
- Changing MX providers requires updating the policy before switching DNS.
- MTA-STS policies are cached for `max_age`; reverting a mistake takes time.

## Verify
- [ ] The policy URL returns the policy over HTTPS with a valid certificate.
- [ ] TLS-RPT reports show no failures from major senders in enforce mode.

## Checked

2026-10-28. Confirmed against: RFC 8461 (policy file, version/mode/mx/max_age, testing and enforce modes, policy cache, id in the DNS record); RFC 8460 (_smtp._tls TLS-RPT record, JSON reports).

Removed as unconfirmed: DANE/TLSA section, Microsoft 365 MX name, provider support claims, report-review duration, example max_age figure, RFC 7672 source.

Method: documentation only; no commands were run.
