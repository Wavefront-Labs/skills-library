---
id: computing-software.cryptography-implementation.protocol-implementation.dns-caa-records
name: dns-caa-records
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, caa-record, dns-caa, rfc-8659, rfc-8657, certificate-issuance, acme, dns, webpki]
level: practitioner
status: docs-checked
description: "Restrict which CAs may issue for your domains with DNS CAA records: issue, issuewild, iodef, RFC 8657 accounturi and validationmethods, and checking them."
sources: ["https://www.rfc-editor.org/rfc/rfc8659", "https://www.rfc-editor.org/rfc/rfc8657", "https://letsencrypt.org/docs/caa/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS CAA records

CAA (RFC 8659) lets a domain owner state which CAs may issue. CAA limits which CA, account
and validation method can obtain certificates for a name.

## Records
```
example.com.  3600 IN CAA 0 issue "letsencrypt.org"
example.com.  3600 IN CAA 0 issue "digicert.com"
example.com.  3600 IN CAA 0 issuewild ";"                          ; no wildcard certificates from anyone
example.com.  3600 IN CAA 0 iodef "mailto:pki-alerts@example.com"
```
- `issue` applies to all names; `issuewild` overrides it for wildcard requests.
- `";"` alone means "no CA may issue".
- CAs walk up the DNS tree: a record on `example.com` covers `api.example.com` unless that name has its own CAA set.
- Flag 128 (critical) on an unknown tag forbids issuance; avoid unless needed.

## Tighter control (RFC 8657)
```
example.com. CAA 0 issue "letsencrypt.org; accounturi=https://acme-v02.api.letsencrypt.org/acme/acct/123456789; validationmethods=dns-01"
```
Only your ACME account, and only via DNS-01, can get certificates. Strong defence against domain-validation attacks
on HTTP paths. Confirm your CA supports these parameters.

## Check
```
dig +short CAA example.com
dig +short CAA api.example.com     # empty means inherits from parent
```

## Gotchas
- Adding CAA without listing the CA your CDN or SaaS provider uses breaks their automatic renewals; inventory every
  CA issuing for you (Certificate Transparency search) first.
- CNAMEs: CAA lookup follows CNAME targets; a `www` CNAME to a provider domain may pick up the provider's CAA.
- DNSSEC is recommended so CAA cannot be spoofed to the CA.

## Verify
- [ ] CT log search shows no certificates from unlisted CAs after rollout.
- [ ] Test issuance from an unlisted CA (staging) is refused.

## Checked
2026-11-01. Confirmed against RFC 8659 (issue, issuewild precedence, `";"` forbids issuance, climbing the DNS tree, critical flag 128, DNSSEC strongly recommended), RFC 8657 (accounturi and validationmethods parameters) and the Let's Encrypt CAA page (CAA checks follow CNAME redirects). Removed: the Baseline Requirements claim, which no fetched page stated.
Method: documentation only; no commands were run.
