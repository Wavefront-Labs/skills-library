---
id: computing-software.systems-network-administration.dns-dhcp.dmarc-policy-rollout
name: dmarc-policy-rollout
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, email-authentication, dmarc, alignment, rua, ruf, aggregate-reports, p-none, p-quarantine, p-reject, pct, sp-tag, bulk-sender-requirements, email-dns]
level: practitioner
status: verified
description: "Roll DMARC from p=none to p=reject safely: record syntax, SPF/DKIM alignment, aggregate report analysis, fixing each sender, staged enforcement, and subdomain policy."
sources:
  - https://datatracker.ietf.org/doc/html/rfc7489
  - https://support.google.com/a/answer/81126
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMARC policy rollout

DMARC ties SPF and DKIM to the visible **From** domain and tells receivers what to do when
neither passes **aligned**. Gmail requires SPF and DKIM plus a DMARC record (policy may be `none`) from senders of more
than 5,000 messages a day to Gmail accounts since 1 Feb 2024 (Google sender guidelines). The base standard is now
RFC 9989 (May 2026, Standards Track, obsoletes RFC 7489); aggregate and failure reporting moved to RFC 9990 and 9991.

## Record
```
_dmarc.example.org. TXT "v=DMARC1; p=none; rua=mailto:dmarc-rua@example.org; fo=1; adkim=r; aspf=r"
```
| Tag | Meaning |
|---|---|
| p | none / quarantine / reject for the domain |
| sp | policy for subdomains (defaults to p) |
| rua | aggregate (daily XML) report destination |
| ruf | failure reports (RFC 9991): receivers decide whether to create them at all, because of privacy considerations |
| np | policy for non-existent subdomains (new in RFC 9989) |
| t | test mode `y` or `n` (default `n`): `y` asks receivers to apply one level below p (reject becomes quarantine, quarantine becomes none) |
| pct | RFC 7489 sampling percentage; marked historic and removed in RFC 9989 (inaccurate except at 0 and 100); `t=y` is roughly `pct=0`, `t=n` is `pct=100` |
| adkim / aspf | r relaxed (organisational domain match) / s strict (exact); default r |
| fo | failure-report options, default 0 |
Pass = (SPF pass AND Return-Path domain aligned) OR (DKIM pass AND d= aligned).
Reports to another domain need that domain to authorise it:
`example.org._report._dmarc.reports.vendor.net TXT "v=DMARC1"`.

## Rollout
1. **p=none** with rua. Collect 2-4 weeks of reports (use a report parser such as the
   open-source parsedmarc).
2. For each source IP/sender in the reports: legitimate? fix SPF include or, better, DKIM signing
   with an aligned d=. Unknown senders sending as you = spoofing (what DMARC will block).
3. **p=quarantine**, using `t=y` (RFC 9989) or, for receivers still on RFC 7489, `pct=25` -> 50 -> 100; receivers
   applied intermediate `pct` values inconsistently, so judge from reports and helpdesk, not from the percentage.
   Then drop `t=y`.
4. **p=reject** once legitimate mail is consistently aligned.
5. Set `sp=reject` (or per-subdomain records) and protect non-sending domains with `p=reject`.

## Gotchas
- Forwarders and mailing lists break SPF (and lists may break DKIM): ARC helps receivers; DKIM
  is the alignment that survives forwarding, so sign everything.
- Third-party senders using their own Return-Path pass SPF but are **not aligned**: they need
  DKIM with your domain or a custom return-path subdomain.
- One `_dmarc` TXT record only.

## Verify
- [ ] Aggregate reports show >= 98-99% aligned pass for legitimate sources before enforcing.
- [ ] Test mail from each system shows `dmarc=pass` in Authentication-Results.
- [ ] Final policy p=reject with sp set; report monitoring continues.
