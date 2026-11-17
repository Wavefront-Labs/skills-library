---
id: computing-software.cybersecurity-defensive.network-defence.dns-caa-records
name: dns-caa-records
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [dns-security, caa-records, certificate-authority-authorization, rfc-8659, mis-issuance, iodef, accounturi]
level: practitioner
status: docs-checked
description: "Restrict which CAs may issue for your domains with CAA records: issue vs issuewild, accounturi and validationmethods, iodef, and inheritance pitfalls."
sources: ["https://datatracker.ietf.org/doc/html/rfc8659", "https://letsencrypt.org/docs/caa/", "https://datatracker.ietf.org/doc/html/rfc8657"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAA records

CAA (RFC 8659) tells public CAs which of them may issue for a domain. CAs must check it before issuance
(CA/B Forum requirement). It reduces mis-issuance risk from a CA you do not use, and from staff or
vendors buying certificates outside policy.

## Syntax
```
example.com.  IN CAA 0 issue "letsencrypt.org"
example.com.  IN CAA 0 issuewild ";"                   ; no wildcard certificates from anyone
example.com.  IN CAA 0 iodef "mailto:pki-team@example.com"
```
- `issue`: allowed CAs for all certificates (including wildcards if no `issuewild` present).
- `issuewild`: overrides `issue` for wildcard certificates; `";"` forbids.
- `iodef`: where CAs may report refused requests (not all do).
- Flag 128 (critical) on unknown tags makes CAs refuse; leave 0 unless you know.

## Tighten further (RFC 8657)
```
example.com. IN CAA 0 issue "letsencrypt.org; accounturi=https://acme-v02.api.letsencrypt.org/acme/acct/123456; validationmethods=dns-01"
```
Only your ACME account, only DNS validation: an attacker who controls a web server on a subdomain
cannot obtain certificates via HTTP-01 with their own account. Check CA support (Let's Encrypt supports both).

## Lookup and inheritance
CAs climb the DNS tree: for `www.shop.example.com` they check that name, then `shop.example.com`, then
`example.com`, using the first CAA RRset found. A CNAME at a name is followed. So:
- A CAA at the apex covers all subdomains unless a subdomain has its own CAA.
- Subdomains delegated to a SaaS via CNAME inherit the target domain's CAA (which may block your CA).

## Rollout
1. Inventory CAs actually used: search certificate transparency logs for your domains.
2. Publish CAA listing all of them; add `iodef`.
3. Remove CAs as teams consolidate; enforce through procurement.

## Gotchas
- Forgetting a CA used by a vendor-hosted service (CDN, email security, SaaS custom domain) breaks
  their renewals; CT logs show which CAs issued for each name.
- DNSSEC is not required but strengthens CAA against spoofed DNS answers to CAs.

## Verify
`dig CAA example.com +short` returns the policy; request a staging cert from a non-listed CA (or use
a CAA test tool) and confirm refusal.

## Checked

2026-10-28. Confirmed against: RFC 8659 (issue, issuewild, iodef, critical flag, tree climbing and CNAME handling); RFC 8657 (accounturi, validationmethods); Let's Encrypt CAA documentation.

Removed as unconfirmed: second CA example record, crt.sh query syntax.

Method: documentation only; no commands were run.
