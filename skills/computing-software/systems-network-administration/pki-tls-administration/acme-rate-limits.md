---
id: computing-software.systems-network-administration.pki-tls-administration.acme-rate-limits
name: acme-rate-limits
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [acme-rate-limits, pki-acme-testing, letsencrypt, rate-limits, ari, renewal-info, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Stay within Let's Encrypt rate limits, use staging, and adopt ACME Renewal Information (ARI) for renewals."
sources:
  - https://letsencrypt.org/docs/rate-limits/
  - https://datatracker.ietf.org/doc/rfc9773/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME rate limits and avoiding them
Goal: no outage because the CA refused to issue.
Let's Encrypt limits as listed on its Rate Limits page (last updated 5 August 2026; re-read it, values change): 300 new orders per account per 3 hours; 50 certificates per registered domain (or IPv4 address, or IPv6 /64) per 7 days; 5 certificates per exact set of identifiers per 7 days; 5 authorization failures per identifier per account per hour. Limits use a token bucket, so capacity refills gradually and cannot be reset.
- Renewals signalled through ARI are exempt from all rate limits. Without ARI, an order with the exact same identifier set counts as a renewal but may still be subject to some limits.
- Do not re-issue from scratch while debugging; use the staging environment (significantly higher limits) and certbot `--dry-run`, which uses staging.
- ARI is RFC 9773: the directory gains a `renewalInfo` URL clients use to learn the suggested renewal window. acme.sh follows it automatically when the CA exposes `renewalInfo`.
- Spread renewal start times rather than renewing everything at once.
Gotcha: reinstalling a client repeatedly, or deleting its configuration on every deploy, is the common way to hit the exact-set limit of 5 per 7 days.
Verify:
- [ ] Rate-limit checks via crt.sh counts for your registered domain are below thresholds.
- [ ] Renewal runs on a regular schedule (certbot's docs suggest running the renew command every day or week; it only renews certificates near expiry).

## Checked
2026-11-03. Confirmed on the Let's Encrypt Rate Limits page: the four limit values above, token bucket, ARI exemption and non-ARI renewal wording, staging recommendation, crt.sh as a way to list issued certificates; RFC 9773 for `renewalInfo`; the acme.sh README for automatic ARI; the certbot usage page for `--dry-run` and the renew schedule. Removed: certbot 4 and lego ARI support, the `shortlived` profile, `RandomizedDelaySec`, the wildcard-plus-apex gotcha and the twice-daily claim. Replaced: the per-hostname failed-validation figure (the page says per identifier per account) and the weekly wording of the exact-set limit.
Method: documentation only; no commands were run.
